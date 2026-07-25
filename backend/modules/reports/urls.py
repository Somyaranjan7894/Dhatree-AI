"""URL routing for Reports Module."""
from django.urls import path
from .views.analytics_views import AnalyticsAPIView

app_name = "reports"

urlpatterns = [
    path("analytics/", AnalyticsAPIView.as_view(), name="analytics_overview"),
]
