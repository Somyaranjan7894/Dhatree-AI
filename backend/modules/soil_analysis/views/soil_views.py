from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from core.permissions import IsAuthenticated, OwnerOnly
from core.responses import success_response
from modules.soil_analysis.serializers.soil_serializers import SoilSampleSerializer
from modules.soil_analysis.services.soil_service import SoilService
from modules.farms.services.farm_service import FarmService

@extend_schema_view(
    list=extend_schema(description="List all soil samples for a specific farm."),
    retrieve=extend_schema(description="Retrieve specific soil sample details."),
    create=extend_schema(description="Add a new soil sample record for a farm."),
)
class SoilSampleViewSet(viewsets.GenericViewSet):
    """ViewSet for managing Soil Samples for a Farm."""
    serializer_class = SoilSampleSerializer
    permission_classes = [IsAuthenticated, OwnerOnly]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.soil_service = SoilService()
        self.farm_service = FarmService()

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return self.soil_service.soil_repository.model_class.active_objects.none()
        if getattr(user, "role", "") == "admin" or user.is_superuser:
            return self.soil_service.soil_repository.model_class.active_objects.all()
        return self.soil_service.soil_repository.model_class.active_objects.filter(farm__owner=user)

    def retrieve(self, request: Request, pk: str = None) -> Response:
        sample = self.soil_service.get_sample(sample_id=pk)
        self.check_object_permissions(request, sample.farm)
        serializer = self.get_serializer(sample)
        return success_response(data=serializer.data, message="Soil sample retrieved successfully.")

    def update(self, request: Request, pk: str = None) -> Response:
        sample = self.soil_service.get_sample(sample_id=pk)
        self.check_object_permissions(request, sample.farm)
        serializer = self.get_serializer(data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        updated_sample = self.soil_service.update_sample(sample_id=pk, **serializer.validated_data)
        return success_response(
            data=SoilSampleSerializer(updated_sample).data,
            message="Soil sample updated successfully.",
        )

    def partial_update(self, request: Request, pk: str = None) -> Response:
        sample = self.soil_service.get_sample(sample_id=pk)
        self.check_object_permissions(request, sample.farm)
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_sample = self.soil_service.update_sample(sample_id=pk, **serializer.validated_data)
        return success_response(
            data=SoilSampleSerializer(updated_sample).data,
            message="Soil sample updated successfully.",
        )

    def destroy(self, request: Request, pk: str = None) -> Response:
        sample = self.soil_service.get_sample(sample_id=pk)
        self.check_object_permissions(request, sample.farm)
        self.soil_service.delete_sample(sample_id=pk)
        return success_response(data={}, message="Soil sample deleted successfully.", status_code=status.HTTP_200_OK)
