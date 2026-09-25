from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsAdmin, IsManager
from employees.models import Employee

from notifications.models import Notification

from .models import LeaveRequest, LeaveType
from .serializers import (
    LeaveRequestSerializer,
    LeaveTypeSerializer,
)


class LeaveTypeListCreateView(generics.ListCreateAPIView):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsManager()]

        return [IsAuthenticated()]


class LeaveTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdmin()]

        if self.request.method in ["PUT", "PATCH"]:
            return [IsManager()]

        return [IsAuthenticated()]


class LeaveRequestListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = LeaveRequestSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        queryset = LeaveRequest.objects.select_related(
            "employee",
            "employee__user",
            "employee__department",
            "leave_type",
            "reviewed_by",
        )

        if user.role not in ["ADMIN", "MANAGER"]:
            queryset = queryset.filter(
                employee__user=user
            )

        search = self.request.query_params.get(
            "search"
        )

        from_date = self.request.query_params.get(
            "from_date"
        )

        to_date = self.request.query_params.get(
            "to_date"
        )

        department = self.request.query_params.get(
            "department"
        )

        employee = self.request.query_params.get(
            "employee"
        )

        leave_type = self.request.query_params.get(
            "leave_type"
        )

        leave_status = self.request.query_params.get(
            "status"
        )

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

        if from_date:
            queryset = queryset.filter(
                from_date__gte=from_date
            )

        if to_date:
            queryset = queryset.filter(
                to_date__lte=to_date
            )

        if department:
            queryset = queryset.filter(
                employee__department_id=department
            )

        if employee:
            queryset = queryset.filter(
                employee_id=employee
            )

        if leave_type:
            queryset = queryset.filter(
                leave_type_id=leave_type
            )

        if leave_status:
            queryset = queryset.filter(
                status=leave_status
            )

        return queryset

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == "EMPLOYEE":
            employee = getattr(
                user,
                "employee_profile",
                None,
            )

            if not employee:
                from rest_framework.exceptions import (
                    ValidationError,
                )

                raise ValidationError(
                    {
                        "employee": (
                            "Your account does not have "
                            "an employee profile."
                        )
                    }
                )

            leave_request = serializer.save(
                employee=employee,
            )

            recipients = user.__class__.objects.filter(
                role__in=["ADMIN", "MANAGER"]
            )

            for recipient in recipients:
                Notification.objects.create(
                    user=recipient,
                    notification_type="LEAVE",
                    title="New Leave Request",
                    message=(
                        f"{user.get_full_name() or user.username} "
                        "has submitted a new leave request."
                    ),
                    related_id=leave_request.id,
                )

            return

        serializer.save()


class LeaveRequestDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = LeaveRequestSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]

        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        queryset = LeaveRequest.objects.select_related(
            "employee",
            "employee__user",
            "employee__department",
            "leave_type",
            "reviewed_by",
        )

        if user.role in ["ADMIN", "MANAGER"]:
            return queryset

        return queryset.filter(
            employee__user=user
        )

    def update(self, request, *args, **kwargs):
        leave_request = self.get_object()

        if request.user.role == "EMPLOYEE":
            if leave_request.status != LeaveRequest.Status.PENDING:
                return Response(
                    {
                        "detail": (
                            "Only pending leave requests "
                            "can be updated."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return super().update(
            request,
            *args,
            **kwargs,
        )

    def destroy(self, request, *args, **kwargs):
        leave_request = self.get_object()

        if request.user.role == "EMPLOYEE":
            if leave_request.status != LeaveRequest.Status.PENDING:
                return Response(
                    {
                        "detail": (
                            "Only pending leave requests "
                            "can be cancelled."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            leave_request.status = (
                LeaveRequest.Status.CANCELLED
            )

            leave_request.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

            return Response(
                {
                    "detail": (
                        "Leave request cancelled successfully."
                    )
                },
                status=status.HTTP_200_OK,
            )

        return super().destroy(
            request,
            *args,
            **kwargs,
        )


class LeaveRequestReviewView(
    generics.UpdateAPIView
):
    serializer_class = LeaveRequestSerializer

    permission_classes = [IsManager]

    queryset = LeaveRequest.objects.select_related(
        "employee",
        "employee__user",
        "employee__department",
        "leave_type",
        "reviewed_by",
    )

    def update(self, request, *args, **kwargs):
        leave_request = self.get_object()

        requested_status = request.data.get("status")

        allowed_statuses = [
            LeaveRequest.Status.APPROVED,
            LeaveRequest.Status.REJECTED,
        ]

        if requested_status not in allowed_statuses:
            return Response(
                {
                    "status": (
                        "Status must be APPROVED or REJECTED."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if leave_request.status != LeaveRequest.Status.PENDING:
            return Response(
                {
                    "detail": (
                        "Only pending leave requests "
                        "can be reviewed."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        leave_request.status = requested_status
        leave_request.reviewed_by = request.user
        leave_request.reviewed_at = timezone.now()
        leave_request.reviewer_remarks = (
            request.data.get(
                "reviewer_remarks",
                "",
            )
        )

        leave_request.save()

        employee_user = leave_request.employee.user

        employee_name = (
            f"{employee_user.first_name} "
            f"{employee_user.last_name}"
        ).strip() or employee_user.username

        if requested_status == LeaveRequest.Status.APPROVED:
            notification_title = "Leave Request Approved"
            notification_message = (
                f"Your leave request #{leave_request.id} "
                "has been approved."
            )
        else:
            notification_title = "Leave Request Rejected"
            notification_message = (
                f"Your leave request #{leave_request.id} "
                "has been rejected."
            )

        Notification.objects.create(
            user=employee_user,
            notification_type="LEAVE",
            title=notification_title,
            message=notification_message,
            related_id=leave_request.id,
        )

        return Response(
            self.get_serializer(
                leave_request
            ).data
        )