from django.urls import path

from .views import (
    AIAssistantView,
    IntelligenceOverviewView,
)

urlpatterns = [
    path(
        "",
        IntelligenceOverviewView.as_view(),
        name="intelligence-overview",
    ),
    path(
        "assistant/",
        AIAssistantView.as_view(),
        name="ai-assistant",
    ),
]