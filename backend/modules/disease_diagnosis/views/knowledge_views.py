from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from modules.disease_diagnosis.models.knowledge import Disease
from modules.disease_diagnosis.serializers.knowledge_serializers import (
    DiseaseSerializer,
)


class DiseaseKnowledgeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides read-only access to the Disease Knowledge Base.
    Supports searching and filtering by crop and severity.
    """

    queryset = Disease.objects.prefetch_related(
        "treatments", "preventions", "references"
    ).all()
    serializer_class = DiseaseSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["crop", "severity"]
    search_fields = ["name", "description", "symptoms"]

    def get_object(self):
        """
        Allow retrieval by either UUID (id) or Exact Disease Name (name).
        """
        lookup_value = self.kwargs[self.lookup_field]

        # Try finding by name first, if it fails, fallback to standard UUID lookup
        try:
            return self.queryset.get(name=lookup_value)
        except Disease.DoesNotExist:
            return super().get_object()
