from django.urls import path

from .views import (
    NotificationListCreateView,
    NotificationMarkAllReadView,
    NotificationMarkReadView,
    NotificationUnreadCountView,
)


urlpatterns = [
    path(
        "",
        NotificationListCreateView.as_view(),
        name="notification-list-create",
    ),

    path(
        "unread-count/",
        NotificationUnreadCountView.as_view(),
        name="notification-unread-count",
    ),

    path(
        "mark-all-read/",
        NotificationMarkAllReadView.as_view(),
        name="notification-mark-all-read",
    ),

    path(
        "<int:notification_id>/read/",
        NotificationMarkReadView.as_view(),
        name="notification-mark-read",
    ),
]