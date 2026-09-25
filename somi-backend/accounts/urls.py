from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    LoginView,
    MeView,
    LogoutView,
    UserManagementListCreateView,
    UserManagementDetailView,
    AdminOnlyTestView,
    ManagerOnlyTestView,
    StaffTestView,
)


urlpatterns = [
    # Authentication
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token-refresh",
    ),
    path(
        "me/",
        MeView.as_view(),
        name="me",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    # User Management
    path(
        "users/",
        UserManagementListCreateView.as_view(),
        name="user-management-list-create",
    ),
    path(
        "users/<int:pk>/",
        UserManagementDetailView.as_view(),
        name="user-management-detail",
    ),

    # Permission testing
    path(
        "test/admin/",
        AdminOnlyTestView.as_view(),
        name="admin-test",
    ),
    path(
        "test/manager/",
        ManagerOnlyTestView.as_view(),
        name="manager-test",
    ),
    path(
        "test/staff/",
        StaffTestView.as_view(),
        name="staff-test",
    ),
]