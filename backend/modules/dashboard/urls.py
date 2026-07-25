"""URL routing for Dashboard Module."""
from django.urls import path
from .views.dashboard_views import DashboardOverviewAPIView
from .views.search_views import GlobalSearchAPIView

app_name = "dashboard"

urlpatterns = [
    path("overview/", DashboardOverviewAPIView.as_view(), name="dashboard_overview"),
    path("search/", GlobalSearchAPIView.as_view(), name="global_search"),
]
