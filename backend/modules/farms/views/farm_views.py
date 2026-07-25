"""
API Views for Farm, FarmCrop, FarmImage, and FarmActivity management.
Delegates all domain processing directly to FarmService and returns standardized JSON responses.
"""

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from core.permissions import IsAuthenticated, OwnerOnly
from core.responses import paginated_response, success_response
from modules.farms.models.farm import Farm
from modules.farms.models.farm_activity import FarmActivity
from modules.farms.models.farm_crop import FarmCrop
from modules.farms.models.farm_image import FarmImage
from modules.farms.serializers.farm_serializers import (
    FarmActivitySerializer,
    FarmCreateUpdateSerializer,
    FarmCropSerializer,
    FarmImageSerializer,
    FarmSerializer,
)
from modules.farms.services.farm_service import (
    FarmActivityService,
    FarmCropService,
    FarmImageService,
    FarmService,
)
from modules.soil_analysis.serializers.soil_serializers import SoilSampleSerializer
from modules.soil_analysis.services.soil_service import SoilService
from modules.weather_intelligence.serializers.weather_serializers import (
    WeatherSnapshotSerializer,
)
from modules.weather_intelligence.services.weather_service import WeatherService


@extend_schema_view(
    list=extend_schema(description="List active farms for the authenticated user."),
    retrieve=extend_schema(description="Retrieve specific farm details by UUID."),
    create=extend_schema(description="Create a new farm profile."),
)
class FarmViewSet(viewsets.GenericViewSet):
    """ViewSet for managing Farm parcels and their nested resources."""

    serializer_class = FarmSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "water_source", "state", "district"]
    search_fields = ["farm_name", "village", "district", "state"]
    ordering_fields = ["created_at", "farm_name", "area"]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.farm_service = FarmService()
        self.crop_service = FarmCropService()
        self.image_service = FarmImageService()
        self.activity_service = FarmActivityService()
        self.soil_service = SoilService()
        self.weather_service = WeatherService()

    def get_permissions(self):
        return [IsAuthenticated(), OwnerOnly()]

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return Farm.active_objects.none()
        if getattr(user, "role", "") == "admin" or user.is_superuser:
            return Farm.active_objects.all()
        return Farm.active_objects.filter(owner=user)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return FarmCreateUpdateSerializer
        return FarmSerializer

    def get_paginated_response(self, data):
        return paginated_response(
            self.paginator, data, message="Farms retrieved successfully."
        )

    def list(self, request: Request) -> Response:
        """List all active farms owned by the user (or all if admin)."""
        user = request.user
        owner_id = (
            None
            if (getattr(user, "role", "") == "admin" or user.is_superuser)
            else user.id
        )
        queryset = self.farm_service.list_farms(owner_id=owner_id)
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FarmSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = FarmSerializer(queryset, many=True)
        return success_response(
            data=serializer.data, message="Farms retrieved successfully."
        )

    def retrieve(self, request: Request, pk: str = None) -> Response:
        """Retrieve a specific farm by ID."""
        farm = self.farm_service.get_farm(farm_id=pk)
        self.check_object_permissions(request, farm)
        serializer = FarmSerializer(farm)
        return success_response(
            data=serializer.data, message="Farm details retrieved successfully."
        )

    def create(self, request: Request) -> Response:
        """Create a new farm parcel profile."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        farm = self.farm_service.create_farm(
            owner=request.user, **serializer.validated_data
        )
        return success_response(
            data=FarmSerializer(farm).data,
            message="Farm created successfully.",
            status_code=status.HTTP_201_CREATED,
        )

    def update(self, request: Request, pk: str = None) -> Response:
        """Update farm profile attributes."""
        farm = self.farm_service.get_farm(farm_id=pk)
        self.check_object_permissions(request, farm)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_farm = self.farm_service.update_farm(
            farm_id=pk, **serializer.validated_data
        )
        return success_response(
            data=FarmSerializer(updated_farm).data,
            message="Farm updated successfully.",
        )

    def partial_update(self, request: Request, pk: str = None) -> Response:
        """Partial update of farm profile attributes."""
        farm = self.farm_service.get_farm(farm_id=pk)
        self.check_object_permissions(request, farm)
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_farm = self.farm_service.update_farm(
            farm_id=pk, **serializer.validated_data
        )
        return success_response(
            data=FarmSerializer(updated_farm).data,
            message="Farm updated successfully.",
        )

    def destroy(self, request: Request, pk: str = None) -> Response:
        """Soft-delete a farm profile."""
        farm = self.farm_service.get_farm(farm_id=pk)
        self.check_object_permissions(request, farm)
        self.farm_service.soft_delete_farm(farm_id=pk)
        return success_response(
            data={},
            message="Farm deleted successfully.",
            status_code=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def archive(self, request: Request, pk: str = None) -> Response:
        """Transition farm status to archived."""
        farm = self.farm_service.get_farm(farm_id=pk)
        self.check_object_permissions(request, farm)
        updated_farm = self.farm_service.archive_farm(farm_id=pk)
        return success_response(
            data=FarmSerializer(updated_farm).data,
            message="Farm archived successfully.",
        )

    @action(detail=True, methods=["get", "post"], url_path="crops")
    def crops(self, request: Request, pk: str = None) -> Response:
        """List or create crop cycles cultivated on this farm."""
        farm = self.farm_service.get_farm(farm_id=pk)
        self.check_object_permissions(request, farm)

        if request.method == "POST":
            serializer = FarmCropSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            crop_id = request.data.get("crop")
            farm_crop = self.crop_service.create_farm_crop(
                farm_id=pk, crop_id=crop_id, **serializer.validated_data
            )
            return success_response(
                data=FarmCropSerializer(farm_crop).data,
                message="Crop cycle added to farm successfully.",
                status_code=status.HTTP_201_CREATED,
            )

        queryset = self.crop_service.list_farm_crops(farm_id=pk)
        return success_response(
            data=FarmCropSerializer(queryset, many=True).data,
            message="Farm crops retrieved successfully.",
        )

    @action(detail=True, methods=["get", "post"], url_path="images")
    def images(self, request: Request, pk: str = None) -> Response:
        """List or upload visual observations for this farm."""
        farm = self.farm_service.get_farm(farm_id=pk)
        self.check_object_permissions(request, farm)

        if request.method == "POST":
            serializer = FarmImageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            farm_image = self.image_service.upload_image(
                farm_id=pk, **serializer.validated_data
            )
            return success_response(
                data=FarmImageSerializer(farm_image).data,
                message="Farm image uploaded successfully.",
                status_code=status.HTTP_201_CREATED,
            )

        queryset = self.image_service.list_images(farm_id=pk)
        return success_response(
            data=FarmImageSerializer(queryset, many=True).data,
            message="Farm images retrieved successfully.",
        )

    @action(detail=True, methods=["get", "post"], url_path="history")
    def history(self, request: Request, pk: str = None) -> Response:
        """List or log historical activity events on this farm."""
        farm = self.farm_service.get_farm(farm_id=pk)
        self.check_object_permissions(request, farm)

        if request.method == "POST":
            serializer = FarmActivitySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            activity = self.activity_service.log_activity(
                farm_id=pk, performed_by=request.user, **serializer.validated_data
            )
            return success_response(
                data=FarmActivitySerializer(activity).data,
                message="Activity logged successfully.",
                status_code=status.HTTP_201_CREATED,
            )

        queryset = self.activity_service.list_activities(farm_id=pk)
        return success_response(
            data=FarmActivitySerializer(queryset, many=True).data,
            message="Farm history activities retrieved successfully.",
        )

    @action(detail=True, methods=["get", "post"], url_path="soil-samples")
    def soil_samples(self, request: Request, pk: str = None) -> Response:
        """List or add soil samples for this farm."""
        farm = self.farm_service.get_farm(farm_id=pk)
        self.check_object_permissions(request, farm)

        if request.method == "POST":
            serializer = SoilSampleSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            sample = self.soil_service.create_sample(
                farm_id=pk, **serializer.validated_data
            )
            return success_response(
                data=SoilSampleSerializer(sample).data,
                message="Soil sample logged successfully.",
                status_code=status.HTTP_201_CREATED,
            )

        queryset = self.soil_service.list_samples(farm_id=pk)
        return success_response(
            data=SoilSampleSerializer(queryset, many=True).data,
            message="Farm soil samples retrieved successfully.",
        )

    @action(detail=True, methods=["get", "post"], url_path="weather-snapshots")
    def weather_snapshots(self, request: Request, pk: str = None) -> Response:
        """List or log weather snapshots for this farm."""
        farm = self.farm_service.get_farm(farm_id=pk)
        self.check_object_permissions(request, farm)

        if request.method == "POST":
            serializer = WeatherSnapshotSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            snapshot = self.weather_service.create_snapshot(
                farm_id=pk, **serializer.validated_data
            )
            return success_response(
                data=WeatherSnapshotSerializer(snapshot).data,
                message="Weather snapshot logged successfully.",
                status_code=status.HTTP_201_CREATED,
            )

        queryset = self.weather_service.list_snapshots(farm_id=pk)
        return success_response(
            data=WeatherSnapshotSerializer(queryset, many=True).data,
            message="Farm weather snapshots retrieved successfully.",
        )


class FarmCropViewSet(viewsets.GenericViewSet):
    """ViewSet for individual FarmCrop cycle updates and deletions."""

    serializer_class = FarmCropSerializer
    permission_classes = [IsAuthenticated, OwnerOnly]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.crop_service = FarmCropService()

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return FarmCrop.active_objects.none()
        if getattr(user, "role", "") == "admin" or user.is_superuser:
            return FarmCrop.active_objects.all()
        return FarmCrop.active_objects.filter(farm__owner=user)

    def retrieve(self, request: Request, pk: str = None) -> Response:
        farm_crop = self.crop_service.get_farm_crop(farm_crop_id=pk)
        self.check_object_permissions(request, farm_crop.farm)
        return success_response(
            data=FarmCropSerializer(farm_crop).data,
            message="Farm crop details retrieved successfully.",
        )

    def update(self, request: Request, pk: str = None) -> Response:
        farm_crop = self.crop_service.get_farm_crop(farm_crop_id=pk)
        self.check_object_permissions(request, farm_crop.farm)
        serializer = FarmCropSerializer(data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        updated = self.crop_service.update_farm_crop(
            farm_crop_id=pk, **serializer.validated_data
        )
        return success_response(
            data=FarmCropSerializer(updated).data,
            message="Farm crop updated successfully.",
        )

    def partial_update(self, request: Request, pk: str = None) -> Response:
        farm_crop = self.crop_service.get_farm_crop(farm_crop_id=pk)
        self.check_object_permissions(request, farm_crop.farm)
        serializer = FarmCropSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = self.crop_service.update_farm_crop(
            farm_crop_id=pk, **serializer.validated_data
        )
        return success_response(
            data=FarmCropSerializer(updated).data,
            message="Farm crop updated successfully.",
        )

    def destroy(self, request: Request, pk: str = None) -> Response:
        farm_crop = self.crop_service.get_farm_crop(farm_crop_id=pk)
        self.check_object_permissions(request, farm_crop.farm)
        self.crop_service.soft_delete_farm_crop(farm_crop_id=pk)
        return success_response(
            data={},
            message="Farm crop deleted successfully.",
            status_code=status.HTTP_200_OK,
        )


class FarmImageViewSet(viewsets.GenericViewSet):
    """ViewSet for individual FarmImage updates and deletions."""

    serializer_class = FarmImageSerializer
    permission_classes = [IsAuthenticated, OwnerOnly]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.image_service = FarmImageService()

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return FarmImage.active_objects.none()
        if getattr(user, "role", "") == "admin" or user.is_superuser:
            return FarmImage.active_objects.all()
        return FarmImage.active_objects.filter(farm__owner=user)

    def retrieve(self, request: Request, pk: str = None) -> Response:
        image = self.image_service.get_image(image_id=pk)
        self.check_object_permissions(request, image.farm)
        return success_response(
            data=FarmImageSerializer(image).data,
            message="Image retrieved successfully.",
        )

    def destroy(self, request: Request, pk: str = None) -> Response:
        image = self.image_service.get_image(image_id=pk)
        self.check_object_permissions(request, image.farm)
        self.image_service.delete_image(image_id=pk)
        return success_response(
            data={},
            message="Image deleted successfully.",
            status_code=status.HTTP_200_OK,
        )


class FarmActivityViewSet(viewsets.GenericViewSet):
    """ViewSet for individual FarmActivity history updates and deletions."""

    serializer_class = FarmActivitySerializer
    permission_classes = [IsAuthenticated, OwnerOnly]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.activity_service = FarmActivityService()

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return FarmActivity.active_objects.none()
        if getattr(user, "role", "") == "admin" or user.is_superuser:
            return FarmActivity.active_objects.all()
        return FarmActivity.active_objects.filter(farm__owner=user)

    def retrieve(self, request: Request, pk: str = None) -> Response:
        activity = self.activity_service.get_activity(activity_id=pk)
        self.check_object_permissions(request, activity.farm)
        return success_response(
            data=FarmActivitySerializer(activity).data,
            message="Activity retrieved successfully.",
        )

    def update(self, request: Request, pk: str = None) -> Response:
        activity = self.activity_service.get_activity(activity_id=pk)
        self.check_object_permissions(request, activity.farm)
        serializer = FarmActivitySerializer(data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        updated = self.activity_service.update_activity(
            activity_id=pk, **serializer.validated_data
        )
        return success_response(
            data=FarmActivitySerializer(updated).data,
            message="Activity updated successfully.",
        )

    def partial_update(self, request: Request, pk: str = None) -> Response:
        activity = self.activity_service.get_activity(activity_id=pk)
        self.check_object_permissions(request, activity.farm)
        serializer = FarmActivitySerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = self.activity_service.update_activity(
            activity_id=pk, **serializer.validated_data
        )
        return success_response(
            data=FarmActivitySerializer(updated).data,
            message="Activity updated successfully.",
        )

    def destroy(self, request: Request, pk: str = None) -> Response:
        activity = self.activity_service.get_activity(activity_id=pk)
        self.check_object_permissions(request, activity.farm)
        self.activity_service.delete_activity(activity_id=pk)
        return success_response(
            data={},
            message="Activity deleted successfully.",
            status_code=status.HTTP_200_OK,
        )
