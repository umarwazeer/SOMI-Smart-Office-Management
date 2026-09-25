from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied

from notifications.models import Notification

from .models import Payroll
from .serializers import PayrollSerializer


class PayrollListCreateView(generics.ListCreateAPIView):
    serializer_class = PayrollSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = Payroll.objects.select_related(
            "employee",
            "employee__user",
            "employee__department",
        )

        # Employees can only see their own payroll records.
        if getattr(user, "role", None) == "EMPLOYEE":
            queryset = queryset.filter(employee__user=user)

        # Optional filters
        search = self.request.query_params.get("search")
        employee_id = self.request.query_params.get("employee")
        department = self.request.query_params.get("department")
        payroll_period = self.request.query_params.get("payroll_period")
        payment_method = self.request.query_params.get("payment_method")
        date_from = self.request.query_params.get("date_from")
        date_to = self.request.query_params.get("date_to")

        if search:
            queryset = queryset.filter(
                Q(employee__employee_id__icontains=search)
                | Q(employee__user__username__icontains=search)
                | Q(employee__user__first_name__icontains=search)
                | Q(employee__user__last_name__icontains=search)
            )

        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)

        if department:
            queryset = queryset.filter(employee__department_id=department)

        if payroll_period:
            queryset = queryset.filter(payroll_period=payroll_period)

        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)

        if date_from:
            queryset = queryset.filter(payment_date__gte=date_from)

        if date_to:
            queryset = queryset.filter(payment_date__lte=date_to)

        return queryset

    def perform_create(self, serializer):
        if getattr(self.request.user, "role", None) not in ["ADMIN", "MANAGER"]:
            raise PermissionDenied(
                "Only administrators and managers can create payroll records."
            )

        payroll = serializer.save()

        employee = payroll.employee
        employee_user = getattr(employee, "user", None)

        if employee_user:
            employee_name = employee_user.get_full_name() or employee_user.username

            Notification.objects.create(
                user=employee_user,
                notification_type="PAYROLL",
                title="Payroll Processed",
                message=(
                    f"Your payroll for {payroll.payment_date.strftime('%B %Y')} "
                    f"has been processed. Total salary: "
                    f"{payroll.total_salary}."
                ),
                related_id=payroll.id,
            )


class PayrollDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PayrollSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        queryset = Payroll.objects.select_related(
            "employee",
            "employee__user",
            "employee__department",
        )

        if getattr(user, "role", None) == "EMPLOYEE":
            return queryset.filter(employee__user=user)

        return queryset

    def perform_update(self, serializer):
        if getattr(self.request.user, "role", None) not in ["ADMIN", "MANAGER"]:
            raise PermissionDenied(
                "Only administrators and managers can update payroll records."
            )

        payroll = serializer.save()

        employee = payroll.employee
        employee_user = getattr(employee, "user", None)

        if employee_user:
            Notification.objects.create(
                user=employee_user,
                notification_type="PAYROLL",
                title="Payroll Updated",
                message=(
                    f"Your payroll for "
                    f"{payroll.payment_date.strftime('%B %Y')} "
                    f"has been updated. Total salary: "
                    f"{payroll.total_salary}."
                ),
                related_id=payroll.id,
            )

    def perform_destroy(self, instance):
        if getattr(self.request.user, "role", None) != "ADMIN":
            raise PermissionDenied(
                "Only administrators can delete payroll records."
            )

        instance.delete()