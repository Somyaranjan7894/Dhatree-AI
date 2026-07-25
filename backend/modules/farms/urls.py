"""
URL routing configuration for the Farms module.
Registers all Farm endpoints under `/api/v1/farms/`.
"""
from rest_framework.routers import DefaultRouter
from modules.farms.views.farm_views import (
    FarmActivityViewSet,
    FarmCropViewSet,
    FarmImageViewSet,
    FarmViewSet,
)

app_name = "farms"

router = DefaultRouter()
router.register(r"crops", FarmCropViewSet, basename="farm-crop")
router.register(r"images", FarmImageViewSet, basename="farm-image")
router.register(r"history", FarmActivityViewSet, basename="farm-activity")
router.register(r"", FarmViewSet, basename="farm")

urlpatterns = router.urls
