from django.urls import path

from .views import (
    AttendanceCheckInView,
    AttendanceCheckOutView,
    AttendanceDetailView,
    AttendanceListCreateView,
)


urlpatterns = [
    path(
        "",
        AttendanceListCreateView.as_view(),
        name="attendance-list-create",
    ),

    path(
        "<int:pk>/",
        AttendanceDetailView.as_view(),
        name="attendance-detail",
    ),

    path(
        "check-in/",
        AttendanceCheckInView.as_view(),
        name="attendance-check-in",
    ),

    path(
        "check-out/",
        AttendanceCheckOutView.as_view(),
        name="attendance-check-out",
    ),
]