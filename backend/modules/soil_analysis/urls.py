from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.soil_views import SoilSampleViewSet

app_name = "soil_analysis"
router = DefaultRouter()
router.register(r"", SoilSampleViewSet, basename="soil-samples")

urlpatterns = router.urls
