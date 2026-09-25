from rest_framework import serializers

from employees.models import Employee

from .models import LeaveRequest, LeaveType


class LeaveTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveType

        fields = [
            "id",
            "name",
            "description",
            "default_days",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_default_days(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Default days cannot be negative."
            )

        return value


class LeaveRequestSerializer(serializers.ModelSerializer):

    employee_name = serializers.SerializerMethodField()

    employee_id = serializers.CharField(
        source="employee.employee_id",
        read_only=True,
    )

    department_name = serializers.CharField(
        source="employee.department.name",
        read_only=True,
    )

    leave_type_name = serializers.CharField(
        source="leave_type.name",
        read_only=True,
    )

    reviewed_by_name = serializers.SerializerMethodField()

    class Meta:
        model = LeaveRequest

        fields = [
            "id",
            "employee",
            "employee_id",
            "employee_name",
            "department_name",
            "leave_type",
            "leave_type_name",
            "request_date",
            "from_date",
            "to_date",
            "total_days",
            "description",
            "status",
            "reviewed_by",
            "reviewed_by_name",
            "reviewed_at",
            "reviewer_remarks",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "employee",
            "employee_id",
            "employee_name",
            "department_name",
            "leave_type_name",
            "total_days",
            "status",
            "reviewed_by",
            "reviewed_by_name",
            "reviewed_at",
            "created_at",
            "updated_at",
        ]

    def get_employee_name(self, obj):
        user = obj.employee.user

        full_name = (
            f"{user.first_name} {user.last_name}"
        ).strip()

        return full_name or user.username

    def get_reviewed_by_name(self, obj):
        if not obj.reviewed_by:
            return None

        full_name = (
            f"{obj.reviewed_by.first_name} "
            f"{obj.reviewed_by.last_name}"
        ).strip()

        return full_name or obj.reviewed_by.username

    def validate(self, attrs):
        from_date = attrs.get(
            "from_date",
            getattr(self.instance, "from_date", None),
        )

        to_date = attrs.get(
            "to_date",
            getattr(self.instance, "to_date", None),
        )

        if from_date and to_date:
            if to_date < from_date:
                raise serializers.ValidationError(
                    {
                        "to_date": (
                            "To date cannot be earlier "
                            "than from date."
                        )
                    }
                )

            total_days = (
                to_date - from_date
            ).days + 1

            if total_days <= 0:
                raise serializers.ValidationError(
                    {
                        "total_days": (
                            "Leave duration must be "
                            "at least one day."
                        )
                    }
                )

            attrs["total_days"] = total_days

        employee = attrs.get(
            "employee",
            getattr(self.instance, "employee", None),
        )

        if employee and not isinstance(employee, Employee):
            raise serializers.ValidationError(
                {
                    "employee": (
                        "A valid employee is required."
                    )
                }
            )

        return attrs

    def create(self, validated_data):
        validated_data["status"] = LeaveRequest.Status.PENDING
        validated_data.pop("reviewed_by", None)
        validated_data.pop("reviewed_at", None)
        validated_data.pop("reviewer_remarks", None)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop("status", None)
        validated_data.pop("reviewed_by", None)
        validated_data.pop("reviewed_at", None)
        validated_data.pop("reviewer_remarks", None)

        return super().update(
            instance,
            validated_data,
        )