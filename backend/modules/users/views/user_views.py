"""
API Views for User management.
Delegates all domain processing directly to UserService and returns standardized JSON responses.
"""

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from core.permissions import IsAdmin, IsAuthenticated
from core.responses import paginated_response, success_response
from modules.users.models.user import User
from modules.users.serializers.user_serializers import (
    UserSerializer,
    UserUpdateSerializer,
)
from modules.users.services.user_service import UserService


@extend_schema_view(
    list=extend_schema(description="List all active platform users (Admin only)."),
    retrieve=extend_schema(description="Retrieve specific user details by UUID."),
)
class UserViewSet(viewsets.GenericViewSet):
    """ViewSet for reading, searching, and managing user profiles."""

    queryset = User.active_objects.all()
    serializer_class = UserSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["role", "account_status", "is_verified"]
    search_fields = ["email", "username", "full_name"]
    ordering_fields = ["created_at", "username"]

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.user_service = UserService()

    def get_permissions(self):
        if self.action in ["list", "destroy"]:
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        return UserSerializer

    def get_paginated_response(self, data):
        return paginated_response(
            self.paginator, data, message="Users retrieved successfully."
        )

    def list(self, request: Request) -> Response:
        """Return paginated list of users filtered by query parameters."""
        queryset = self.user_service.list_users()
        queryset = self.filter_queryset(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data, message="Users retrieved successfully."
        )

    def retrieve(self, request: Request, pk: str = None) -> Response:
        """Retrieve a specific user's profile by ID."""
        user = self.user_service.get_user_profile(user_id=pk)
        serializer = self.get_serializer(user)
        return success_response(
            data=serializer.data, message="User profile retrieved successfully."
        )

    @action(detail=False, methods=["get"])
    def me(self, request: Request) -> Response:
        """Retrieve the currently authenticated user's profile."""
        serializer = self.get_serializer(request.user)
        return success_response(
            data=serializer.data, message="Profile retrieved successfully."
        )

    def update(self, request: Request, pk: str = None) -> Response:
        """Full update of user profile attributes."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.user_service.update_user_profile(
            user_id=pk, **serializer.validated_data
        )
        return success_response(
            data=UserSerializer(user).data, message="Profile updated successfully."
        )

    def partial_update(self, request: Request, pk: str = None) -> Response:
        """Partial update of user profile attributes."""
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = self.user_service.update_user_profile(
            user_id=pk, **serializer.validated_data
        )
        return success_response(
            data=UserSerializer(user).data, message="Profile updated successfully."
        )

    def destroy(self, request: Request, pk: str = None) -> Response:
        """Soft-delete a user account (Admin only)."""
        self.user_service.soft_delete_user_account(user_id=pk)
        return success_response(
            data={},
            message="Account deactivated successfully.",
            status_code=status.HTTP_200_OK,
        )
