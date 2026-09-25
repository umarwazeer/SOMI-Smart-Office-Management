from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_active_account",
        "created_at",
    )

    list_filter = (
        "role",
        "is_active",
        "is_active_account",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "SOMI Information",
            {
                "fields": (
                    "role",
                    "phone",
                    "profile_picture",
                    "is_active_account",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "SOMI Information",
            {
                "fields": (
                    "email",
                    "role",
                    "phone",
                    "profile_picture",
                    "is_active_account",
                )
            },
        ),
    )