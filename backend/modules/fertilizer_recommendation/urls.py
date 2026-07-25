from django.urls import path, include
from rest_framework.routers import DefaultRouter
from modules.fertilizer_recommendation.views.recommendation_views import FertilizerRecommendationViewSet

router = DefaultRouter()
router.register(r'predictions', FertilizerRecommendationViewSet, basename='fertilizer-prediction')

app_name = 'fertilizer_recommendation'

urlpatterns = [
    path('', include(router.urls)),
]
