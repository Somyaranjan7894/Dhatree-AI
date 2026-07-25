from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from core.permissions import AdminOrReadOnly, IsAdmin
from core.responses import paginated_response, success_response
from modules.crops.serializers.crop_serializers import CropSerializer
from modules.crops.services.crop_service import CropService


@extend_schema_view(
    list=extend_schema(description="List all available crops."),
    retrieve=extend_schema(description="Retrieve specific crop details."),
    create=extend_schema(
        description="Add a new crop to the master directory (Admin only)."
    ),
)
class CropViewSet(viewsets.GenericViewSet):
    """ViewSet for managing global Crop Master data."""

    serializer_class = CropSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["season", "category"]
    search_fields = ["crop_name", "scientific_name"]
    ordering_fields = ["crop_name", "created_at"]

    # Read-only for regular users, admin required for mutation
    permission_classes = [AdminOrReadOnly]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.crop_service = CropService()

    def get_queryset(self):
        return self.crop_service.list_crops()

    def get_paginated_response(self, data):
        return paginated_response(
            self.paginator, data, message="Crops retrieved successfully."
        )

    def list(self, request: Request) -> Response:
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data, message="Crops retrieved successfully."
        )

    def retrieve(self, request: Request, pk: str = None) -> Response:
        crop = self.crop_service.get_crop(crop_id=pk)
        serializer = self.get_serializer(crop)
        return success_response(
            data=serializer.data, message="Crop details retrieved successfully."
        )

    def create(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        crop = self.crop_service.create_crop(**serializer.validated_data)
        return success_response(
            data=CropSerializer(crop).data,
            message="Crop created successfully.",
            status_code=status.HTTP_201_CREATED,
        )

    def update(self, request: Request, pk: str = None) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_crop = self.crop_service.update_crop(
            crop_id=pk, **serializer.validated_data
        )
        return success_response(
            data=CropSerializer(updated_crop).data,
            message="Crop updated successfully.",
        )

    def partial_update(self, request: Request, pk: str = None) -> Response:
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_crop = self.crop_service.update_crop(
            crop_id=pk, **serializer.validated_data
        )
        return success_response(
            data=CropSerializer(updated_crop).data,
            message="Crop updated successfully.",
        )

    def destroy(self, request: Request, pk: str = None) -> Response:
        self.crop_service.delete_crop(crop_id=pk)
        return success_response(
            data={},
            message="Crop deleted successfully.",
            status_code=status.HTTP_200_OK,
        )
