from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views.weather_views import WeatherSnapshotViewSet

app_name = "weather_intelligence"
router = DefaultRouter()
router.register(r"", WeatherSnapshotViewSet, basename="weather-snapshots")

urlpatterns = router.urls
