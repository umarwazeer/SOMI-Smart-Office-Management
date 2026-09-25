from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    employee_name = serializers.SerializerMethodField()

    employee_id = serializers.CharField(
        source="assigned_to.employee_id",
        read_only=True
    )

    department_name = serializers.CharField(
        source="assigned_to.department.name",
        read_only=True
    )

    class Meta:
        model = Task

        fields = [
            "id",
            "title",
            "description",
            "assigned_to",
            "employee_id",
            "employee_name",
            "department_name",
            "priority",
            "status",
            "start_date",
            "due_date",
            "completed_at",
            "estimated_hours",
            "actual_hours",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "employee_id",
            "employee_name",
            "department_name",
            "completed_at",
            "created_at",
            "updated_at",
        ]

    def get_employee_name(self, obj):
        user = obj.assigned_to.user

        full_name = (
            f"{user.first_name} "
            f"{user.last_name}"
        ).strip()

        return full_name or user.username

    def validate_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Task title is required."
            )

        return value

    def validate_description(self, value):
        if value is None:
            return value

        value = value.strip()

        return value

    def validate(self, attrs):
        start_date = attrs.get(
            "start_date",
            getattr(self.instance, "start_date", None)
        )

        due_date = attrs.get(
            "due_date",
            getattr(self.instance, "due_date", None)
        )

        estimated_hours = attrs.get(
            "estimated_hours",
            getattr(self.instance, "estimated_hours", None)
        )

        actual_hours = attrs.get(
            "actual_hours",
            getattr(self.instance, "actual_hours", None)
        )

        if start_date and due_date and due_date < start_date:
            raise serializers.ValidationError({
                "due_date": (
                    "Due date cannot be earlier than "
                    "the start date."
                )
            })

        if estimated_hours is not None and estimated_hours < 0:
            raise serializers.ValidationError({
                "estimated_hours": (
                    "Estimated hours cannot be negative."
                )
            })

        if actual_hours is not None and actual_hours < 0:
            raise serializers.ValidationError({
                "actual_hours": (
                    "Actual hours cannot be negative."
                )
            })

        return attrs