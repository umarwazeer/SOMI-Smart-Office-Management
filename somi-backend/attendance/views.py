from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from accounts.permissions import IsManager

from .models import Attendance
from .serializers import AttendanceSerializer


class AttendanceListCreateView(generics.ListCreateAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        user = self.request.user

        queryset = Attendance.objects.select_related(
            "employee",
            "employee__user",
            "employee__department",
            "marked_by",
        )

        # Admin and Manager can view all attendance.
        if user.role not in ["ADMIN", "MANAGER"]:
            queryset = queryset.filter(
                employee__user=user
            )

        search = self.request.query_params.get("search")
        from_date = self.request.query_params.get("from_date")
        to_date = self.request.query_params.get("to_date")
        department = self.request.query_params.get("department")
        attendance_status = self.request.query_params.get("status")
        employee = self.request.query_params.get("employee")

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
                date__gte=from_date
            )

        if to_date:
            queryset = queryset.filter(
                date__lte=to_date
            )

        if department:
            queryset = queryset.filter(
                employee__department_id=department
            )

        if attendance_status:
            queryset = queryset.filter(
                status=attendance_status
            )

        if employee:
            queryset = queryset.filter(
                employee_id=employee
            )

        return queryset

    def get_permissions(self):
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user

        # Employee can only create attendance
        # for their own employee profile.
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

            serializer.save(
                marked_by=user,
                employee=employee,
            )
            return

        serializer.save(
            marked_by=user
        )


class AttendanceDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = AttendanceSerializer

    queryset = Attendance.objects.select_related(
        "employee",
        "employee__user",
        "employee__department",
        "marked_by",
    )

    def get_permissions(self):
        if self.request.method in [
            "PUT",
            "PATCH",
            "DELETE",
        ]:
            return [IsManager()]

        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        queryset = super().get_queryset()

        if user.role in ["ADMIN", "MANAGER"]:
            return queryset

        return queryset.filter(
            employee__user=user
        )


class AttendanceCheckInView(generics.CreateAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        employee = getattr(
            user,
            "employee_profile",
            None,
        )

        if not employee:
            return Response(
                {
                    "detail": (
                        "Your account does not have "
                        "an employee profile."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        today = timezone.localdate()
        current_time = timezone.localtime().time()

        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={
                "status": Attendance.Status.PRESENT,
                "check_in_time": current_time,
                "marked_by": user,
            },
        )

        if not created and attendance.check_in_time:
            return Response(
                {
                    "detail": (
                        "You have already checked in today."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not created:
            attendance.check_in_time = current_time
            attendance.status = Attendance.Status.PRESENT
            attendance.marked_by = user
            attendance.save()

        return Response(
            AttendanceSerializer(attendance).data,
            status=status.HTTP_201_CREATED,
        )


class AttendanceCheckOutView(
    generics.UpdateAPIView
):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Attendance.objects.select_related(
            "employee",
            "employee__user",
            "employee__department",
            "marked_by",
        ).filter(
            employee__user=self.request.user,
            date=timezone.localdate(),
        )

    def update(self, request, *args, **kwargs):
        attendance = self.get_queryset().first()

        if not attendance:
            return Response(
                {
                    "detail": (
                        "You have not checked in today."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if attendance.check_out_time:
            return Response(
                {
                    "detail": (
                        "You have already checked out today."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        attendance.check_out_time = (
            timezone.localtime().time()
        )
        attendance.save()

        return Response(
            AttendanceSerializer(attendance).data
        )