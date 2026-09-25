from rest_framework import serializers

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    full_name = serializers.SerializerMethodField()

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    # Write-only upload field.
    # We handle the actual User.profile_picture update
    # manually in create() and update().
    profile_picture = serializers.ImageField(
        required=False,
        allow_null=True,
        write_only=True
    )

    department_name = serializers.CharField(
        source="department.name",
        read_only=True
    )

    class Meta:
        model = Employee

        fields = [
            "id",
            "employee_id",
            "user",
            "username",
            "full_name",
            "email",
            "profile_picture",
            "department",
            "department_name",
            "job_title",
            "phone",
            "address",
            "date_of_birth",
            "joining_date",
            "employment_type",
            "status",
            "salary",
            "emergency_contact_name",
            "emergency_contact_phone",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "username",
            "full_name",
            "email",
            "department_name",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["profile_picture"] = None

        if instance.user and instance.user.profile_picture:
            data["profile_picture"] = (
                instance.user.profile_picture.url
            )

        return data

    def create(self, validated_data):
        profile_picture = validated_data.pop(
            "profile_picture",
            None
        )

        employee = Employee.objects.create(
            **validated_data
        )

        if profile_picture is not None:
            employee.user.profile_picture = profile_picture

            employee.user.save(
                update_fields=["profile_picture"]
            )

        return employee

    def update(self, instance, validated_data):
        profile_picture = validated_data.pop(
            "profile_picture",
            serializers.empty
        )

        employee = super().update(
            instance,
            validated_data
        )

        if profile_picture is not serializers.empty:
            employee.user.profile_picture = profile_picture

            employee.user.save(
                update_fields=["profile_picture"]
            )

        return employee

    def get_full_name(self, obj):
        full_name = (
            f"{obj.user.first_name} "
            f"{obj.user.last_name}"
        ).strip()

        return full_name or obj.user.username

    def validate_employee_id(self, value):
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError(
                "Employee ID is required."
            )

        return value

    def validate_job_title(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Job title is required."
            )

        return value

    def validate_user(self, value):
        if not value.is_active:
            raise serializers.ValidationError(
                "The selected user account is inactive."
            )

        if hasattr(value, "employee_profile"):
            raise serializers.ValidationError(
                "This user already has an employee profile."
            )

        return value

    def validate_department(self, value):
        if value and not value.is_active:
            raise serializers.ValidationError(
                "Cannot assign an employee to an inactive department."
            )

        return value