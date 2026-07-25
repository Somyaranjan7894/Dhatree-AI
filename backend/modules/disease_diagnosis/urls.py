from django.urls import include, path
from rest_framework.routers import DefaultRouter

from modules.disease_diagnosis.views.knowledge_views import DiseaseKnowledgeViewSet

router = DefaultRouter()
router.register(r"knowledge", DiseaseKnowledgeViewSet, basename="disease-knowledge")

app_name = "disease_diagnosis"

urlpatterns = [
    path("", include(router.urls)),
]
