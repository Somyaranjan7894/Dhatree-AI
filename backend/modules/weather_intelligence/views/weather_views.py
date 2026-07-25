from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from core.permissions import IsAuthenticated, OwnerOnly
from core.responses import success_response
from modules.weather_intelligence.serializers.weather_serializers import (
    WeatherSnapshotSerializer,
)
from modules.weather_intelligence.services.weather_service import WeatherService


@extend_schema_view(
    list=extend_schema(description="List all weather snapshots for a specific farm."),
    retrieve=extend_schema(description="Retrieve specific weather snapshot details."),
    create=extend_schema(description="Add a new weather snapshot for a farm."),
)
class WeatherSnapshotViewSet(viewsets.GenericViewSet):
    """ViewSet for managing Weather Snapshots for a Farm."""

    serializer_class = WeatherSnapshotSerializer
    permission_classes = [IsAuthenticated, OwnerOnly]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.weather_service = WeatherService()

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return (
                self.weather_service.weather_repository.model_class.active_objects.none()
            )
        if getattr(user, "role", "") == "admin" or user.is_superuser:
            return (
                self.weather_service.weather_repository.model_class.active_objects.all()
            )
        return (
            self.weather_service.weather_repository.model_class.active_objects.filter(
                farm__owner=user
            )
        )

    def retrieve(self, request: Request, pk: str = None) -> Response:
        snapshot = self.weather_service.get_snapshot(snapshot_id=pk)
        self.check_object_permissions(request, snapshot.farm)
        serializer = self.get_serializer(snapshot)
        return success_response(
            data=serializer.data, message="Weather snapshot retrieved successfully."
        )

    def update(self, request: Request, pk: str = None) -> Response:
        snapshot = self.weather_service.get_snapshot(snapshot_id=pk)
        self.check_object_permissions(request, snapshot.farm)
        serializer = self.get_serializer(data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        updated_snapshot = self.weather_service.update_snapshot(
            snapshot_id=pk, **serializer.validated_data
        )
        return success_response(
            data=WeatherSnapshotSerializer(updated_snapshot).data,
            message="Weather snapshot updated successfully.",
        )

    def partial_update(self, request: Request, pk: str = None) -> Response:
        snapshot = self.weather_service.get_snapshot(snapshot_id=pk)
        self.check_object_permissions(request, snapshot.farm)
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_snapshot = self.weather_service.update_snapshot(
            snapshot_id=pk, **serializer.validated_data
        )
        return success_response(
            data=WeatherSnapshotSerializer(updated_snapshot).data,
            message="Weather snapshot updated successfully.",
        )

    def destroy(self, request: Request, pk: str = None) -> Response:
        snapshot = self.weather_service.get_snapshot(snapshot_id=pk)
        self.check_object_permissions(request, snapshot.farm)
        self.weather_service.delete_snapshot(snapshot_id=pk)
        return success_response(
            data={},
            message="Weather snapshot deleted successfully.",
            status_code=status.HTTP_200_OK,
        )
