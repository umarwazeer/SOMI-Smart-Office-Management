from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to users with ADMIN role.
    """

    message = "Admin access is required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "ADMIN"
        )


class IsManager(BasePermission):
    """
    Allows access to ADMIN and MANAGER users.
    """

    message = "Manager or Admin access is required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ["ADMIN", "MANAGER"]
        )


class IsEmployee(BasePermission):
    """
    Allows access to authenticated employees.
    """

    message = "Employee access is required."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "EMPLOYEE"
        )


class IsStaffMember(BasePermission):
    """
    Allows access to any authenticated SOMI user.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_active_account
        )