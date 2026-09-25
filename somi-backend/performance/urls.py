from django.urls import path

from .views import (
    PerformanceReviewListCreateView,
    PerformanceReviewDetailView,
)


urlpatterns = [
    path(
        "",
        PerformanceReviewListCreateView.as_view(),
        name="performance-list-create",
    ),
    path(
        "<int:pk>/",
        PerformanceReviewDetailView.as_view(),
        name="performance-detail",
    ),
]