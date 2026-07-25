from django.urls import path, include
from rest_framework.routers import DefaultRouter
from modules.crop_recommendation.views.recommendation_views import CropRecommendationViewSet

app_name = "crop_recommendation"

router = DefaultRouter()
router.register(r'predictions', CropRecommendationViewSet, basename='crop-prediction')

urlpatterns = [
    path('', include(router.urls)),
]
