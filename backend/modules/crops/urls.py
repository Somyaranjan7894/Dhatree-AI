from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views.crop_views import CropViewSet

app_name = "crops"
router = DefaultRouter()
router.register(r"", CropViewSet, basename="crops")

urlpatterns = router.urls
