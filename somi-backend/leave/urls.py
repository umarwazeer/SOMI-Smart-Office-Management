from django.urls import path

from .views import (
    LeaveRequestDetailView,
    LeaveRequestListCreateView,
    LeaveRequestReviewView,
    LeaveTypeDetailView,
    LeaveTypeListCreateView,
)


urlpatterns = [
    path(
        "types/",
        LeaveTypeListCreateView.as_view(),
        name="leave-type-list-create",
    ),
    path(
        "types/<int:pk>/",
        LeaveTypeDetailView.as_view(),
        name="leave-type-detail",
    ),
    path(
        "requests/",
        LeaveRequestListCreateView.as_view(),
        name="leave-request-list-create",
    ),
    path(
        "requests/<int:pk>/",
        LeaveRequestDetailView.as_view(),
        name="leave-request-detail",
    ),
    path(
        "requests/<int:pk>/review/",
        LeaveRequestReviewView.as_view(),
        name="leave-request-review",
    ),
]