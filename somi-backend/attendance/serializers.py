from rest_framework import serializers

from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    employee_id = serializers.CharField(
        source="employee.employee_id",
        read_only=True,
    )
    department_name = serializers.CharField(
        source="employee.department.name",
        read_only=True,
    )
    marked_by_name = serializers.SerializerMethodField()

    class Meta:
        model = Attendance

        fields = [
            "id",
            "employee",
            "employee_id",
            "employee_name",
            "department_name",
            "date",
            "status",
            "check_in_time",
            "check_out_time",
            "notes",
            "marked_by",
            "marked_by_name",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "employee_id",
            "employee_name",
            "department_name",
            "marked_by",
            "marked_by_name",
            "created_at",
            "updated_at",
        ]

    def get_employee_name(self, obj):
        user = obj.employee.user

        full_name = (
            f"{user.first_name} {user.last_name}"
        ).strip()

        return full_name or user.username

    def get_marked_by_name(self, obj):
        if not obj.marked_by:
            return None

        full_name = (
            f"{obj.marked_by.first_name} "
            f"{obj.marked_by.last_name}"
        ).strip()

        return full_name or obj.marked_by.username

    def validate(self, attrs):
        employee = attrs.get(
            "employee",
            getattr(self.instance, "employee", None),
        )

        date = attrs.get(
            "date",
            getattr(self.instance, "date", None),
        )

        if employee and date:
            queryset = Attendance.objects.filter(
                employee=employee,
                date=date,
            )

            if self.instance:
                queryset = queryset.exclude(
                    pk=self.instance.pk
                )

            if queryset.exists():
                raise serializers.ValidationError(
                    {
                        "date": (
                            "Attendance for this employee "
                            "already exists for this date."
                        )
                    }
                )

        check_in = attrs.get(
            "check_in_time",
            getattr(self.instance, "check_in_time", None),
        )

        check_out = attrs.get(
            "check_out_time",
            getattr(self.instance, "check_out_time", None),
        )

        if check_in and check_out and check_out < check_in:
            raise serializers.ValidationError(
                {
                    "check_out_time": (
                        "Check-out time cannot be earlier "
                        "than check-in time."
                    )
                }
            )

        return attrs