from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsAdmin, IsManager
from notifications.models import Notification

from .models import PerformanceReview
from .serializers import PerformanceReviewSerializer


class PerformanceReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = PerformanceReviewSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]

        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        queryset = PerformanceReview.objects.select_related(
            "employee",
            "employee__user",
            "employee__department",
        )

        if user.role == "EMPLOYEE":
            queryset = queryset.filter(
                employee__user=user
            )

        search = self.request.query_params.get("search")
        review_period = self.request.query_params.get("review_period")
        review_status = self.request.query_params.get("status")
        employee = self.request.query_params.get("employee")
        department = self.request.query_params.get("department")
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        if search:
            queryset = queryset.filter(
                employee__employee_id__icontains=search
            ) | queryset.filter(
                employee__user__username__icontains=search
            ) | queryset.filter(
                employee__user__first_name__icontains=search
            ) | queryset.filter(
                employee__user__last_name__icontains=search
            )

        if review_period:
            queryset = queryset.filter(
                review_period=review_period
            )

        if review_status:
            queryset = queryset.filter(
                status=review_status
            )

        if employee:
            queryset = queryset.filter(
                employee_id=employee
            )

        if department:
            queryset = queryset.filter(
                employee__department_id=department
            )

        if date_from:
            queryset = queryset.filter(
                review_date__gte=date_from
            )

        if date_to:
            queryset = queryset.filter(
                review_date__lte=date_to
            )

        return queryset.distinct()

    def perform_create(self, serializer):
        review = serializer.save()

        employee_user = review.employee.user

        if review.status == PerformanceReview.Status.SUBMITTED:
            title = "Performance Review Submitted"
            message = (
                "Your performance review has been submitted "
                "and is available for your review."
            )
        else:
            title = "Performance Review Created"
            message = (
                "A new performance review has been created "
                "for you."
            )

        Notification.objects.create(
            user=employee_user,
            notification_type="PERFORMANCE",
            title=title,
            message=message,
            related_id=review.id,
        )


class PerformanceReviewDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = PerformanceReviewSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdmin()]

        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        queryset = PerformanceReview.objects.select_related(
            "employee",
            "employee__user",
            "employee__department",
        )

        if user.role == "EMPLOYEE":
            queryset = queryset.filter(
                employee__user=user
            )

        return queryset

    def update(self, request, *args, **kwargs):
        review = self.get_object()

        if request.user.role == "EMPLOYEE":
            allowed_fields = {
                "employee_comments",
                "status",
            }

            submitted_fields = set(request.data.keys())

            restricted_fields = (
                submitted_fields - allowed_fields
            )

            if restricted_fields:
                return Response(
                    {
                        "detail": (
                            "Employees can only update "
                            "their comments and review status."
                        ),
                        "restricted_fields": sorted(
                            restricted_fields
                        ),
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        old_status = review.status

        response = super().update(
            request,
            *args,
            **kwargs,
        )

        updated_review = self.get_object()
        new_status = updated_review.status

        if new_status != old_status:
            self._create_status_notification(
                updated_review,
                old_status,
                new_status,
            )

        return response

    def _create_status_notification(
        self,
        review,
        old_status,
        new_status,
    ):
        employee_user = review.employee.user

        # Employee acknowledges the review.
        if new_status == PerformanceReview.Status.ACKNOWLEDGED:
            managers = review.employee.user.__class__.objects.filter(
                role__in=["ADMIN", "MANAGER"]
            )

            for manager in managers:
                Notification.objects.create(
                    user=manager,
                    notification_type="PERFORMANCE",
                    title="Performance Review Acknowledged",
                    message=(
                        f"{self._employee_name(review)} "
                        f"has acknowledged performance review "
                        f"#{review.id}."
                    ),
                    related_id=review.id,
                )

            return

        # Manager submits a draft review.
        if (
            new_status == PerformanceReview.Status.SUBMITTED
            and old_status != PerformanceReview.Status.SUBMITTED
        ):
            Notification.objects.create(
                user=employee_user,
                notification_type="PERFORMANCE",
                title="Performance Review Submitted",
                message=(
                    "Your performance review has been submitted "
                    "and is available for your review."
                ),
                related_id=review.id,
            )

    def _employee_name(self, review):
        user = review.employee.user

        full_name = (
            f"{user.first_name} "
            f"{user.last_name}"
        ).strip()

        return full_name or user.username