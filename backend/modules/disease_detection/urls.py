"""URL routing for Disease Detection Module."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.prediction_views import DiseasePredictionViewSet

app_name = "disease_detection"

router = DefaultRouter()
router.register(r'predictions', DiseasePredictionViewSet, basename='disease-prediction')

urlpatterns = [
    path('', include(router.urls)),
]
