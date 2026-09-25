from django.urls import path

from .views import PayrollDetailView, PayrollListCreateView


urlpatterns = [
    path(
        "",
        PayrollListCreateView.as_view(),
        name="payroll-list-create",
    ),
    path(
        "<int:pk>/",
        PayrollDetailView.as_view(),
        name="payroll-detail",
    ),
]