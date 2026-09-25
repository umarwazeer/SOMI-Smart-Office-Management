from rest_framework import serializers

from accounts.models import User
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    manager_name = serializers.SerializerMethodField()

    class Meta:
        model = Department

        fields = [
            "id",
            "name",
            "code",
            "description",
            "manager",
            "manager_name",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "manager_name",
            "created_at",
            "updated_at",
        ]

    def get_manager_name(self, obj):
        if obj.manager:
            full_name = (
                f"{obj.manager.first_name} "
                f"{obj.manager.last_name}"
            ).strip()

            return full_name or obj.manager.username

        return None

    def validate_code(self, value):
        return value.strip().upper()

    def validate_name(self, value):
        return value.strip()

    def validate_manager(self, value):
        if value and value.role not in [
            User.Role.ADMIN,
            User.Role.MANAGER,
        ]:
            raise serializers.ValidationError(
                "Department manager must be an Admin or Manager."
            )

        return value