from django.urls import path
from rest_framework.routers import DefaultRouter
from .views.assistant_views import ChatViewSet

app_name = "ai_assistant"
router = DefaultRouter()
router.register(r"", ChatViewSet, basename="assistant")

urlpatterns = router.urls
