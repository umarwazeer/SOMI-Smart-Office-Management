from rest_framework import serializers

from .models import Payroll


class PayrollSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(
        source="employee.user.get_full_name",
        read_only=True,
    )
    employee_id = serializers.CharField(
        source="employee.employee_id",
        read_only=True,
    )
    department_name = serializers.CharField(
        source="employee.department.name",
        read_only=True,
    )

    class Meta:
        model = Payroll
        fields = [
            "id",
            "employee",
            "employee_name",
            "employee_id",
            "department_name",
            "payroll_period",
            "basic_salary",
            "other_allowances",
            "deductions",
            "total_salary",
            "payment_date",
            "payment_method",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "employee_name",
            "employee_id",
            "department_name",
            "total_salary",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        basic_salary = attrs.get(
            "basic_salary",
            getattr(self.instance, "basic_salary", 0),
        )
        other_allowances = attrs.get(
            "other_allowances",
            getattr(self.instance, "other_allowances", 0),
        )
        deductions = attrs.get(
            "deductions",
            getattr(self.instance, "deductions", 0),
        )

        if basic_salary < 0:
            raise serializers.ValidationError(
                {"basic_salary": "Basic salary cannot be negative."}
            )

        if other_allowances < 0:
            raise serializers.ValidationError(
                {"other_allowances": "Other allowances cannot be negative."}
            )

        if deductions < 0:
            raise serializers.ValidationError(
                {"deductions": "Deductions cannot be negative."}
            )

        total_salary = basic_salary + other_allowances - deductions

        if total_salary < 0:
            raise serializers.ValidationError(
                "Deductions cannot be greater than the total earnings."
            )

        attrs["total_salary"] = total_salary

        return attrs