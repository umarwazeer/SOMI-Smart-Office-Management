from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "api/auth/",
        include("accounts.urls"),
    ),

    path(
        "api/departments/",
        include("departments.urls"),
    ),

    path(
        "api/employees/",
        include("employees.urls"),
    ),

    path(
        "api/attendance/",
        include("attendance.urls"),
    ),

    path(
        "api/leave/",
        include("leave.urls"),
    ),

    path(
        "api/payroll/",
        include("payroll.urls"),
    ),

    path(
        "api/tasks/",
        include("tasks.urls"),
    ),

    path(
        "api/performance/",
        include("performance.urls"),
    ),

    path(
        "api/notifications/",
        include("notifications.urls"),
    ),

    path(
        "api/intelligence/",
        include("intelligence.urls"),
    ),
]


# Serve uploaded media files during development.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )