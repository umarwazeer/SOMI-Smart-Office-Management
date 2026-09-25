from rest_framework import serializers

from .models import PerformanceReview


class PerformanceReviewSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    employee_id = serializers.CharField(
        source="employee.employee_id",
        read_only=True,
    )
    department_name = serializers.CharField(
        source="employee.department.name",
        read_only=True,
    )

    class Meta:
        model = PerformanceReview
        fields = [
            "id",
            "employee",
            "employee_id",
            "employee_name",
            "department_name",
            "review_period",
            "review_date",
            "rating",
            "goals_score",
            "productivity_score",
            "quality_score",
            "teamwork_score",
            "communication_score",
            "strengths",
            "improvement_areas",
            "manager_feedback",
            "employee_comments",
            "status",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "employee_id",
            "employee_name",
            "department_name",
            "created_at",
            "updated_at",
        ]

    def get_employee_name(self, obj):
        user = obj.employee.user

        full_name = f"{user.first_name} {user.last_name}".strip()

        return full_name or user.username

    def validate_employee(self, value):
        if value.status == "INACTIVE":
            raise serializers.ValidationError(
                "Performance review cannot be created for an inactive employee."
            )

        return value

    def validate(self, attrs):
        score_fields = [
            "rating",
            "goals_score",
            "productivity_score",
            "quality_score",
            "teamwork_score",
            "communication_score",
        ]

        errors = {}

        for field in score_fields:
            value = attrs.get(
                field,
                getattr(self.instance, field, None) if self.instance else None,
            )

            if value is None:
                continue

            if value < 0 or value > 10:
                errors[field] = "Score must be between 0 and 10."

        if errors:
            raise serializers.ValidationError(errors)

        return attrs