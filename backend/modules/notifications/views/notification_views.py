from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from core.permissions import IsAuthenticated
from core.responses import success_response
from modules.notifications.serializers.notification_serializers import (
    NotificationSerializer,
)
from modules.notifications.services.notification_service import NotificationService


@extend_schema_view(
    list=extend_schema(
        description="List all notifications for the authenticated user."
    ),
    retrieve=extend_schema(description="Retrieve specific notification details."),
)
class NotificationViewSet(viewsets.GenericViewSet):
    """ViewSet for managing user Notifications."""

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notification_service = NotificationService()

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return (
                self.notification_service.notification_repository.model_class.active_objects.none()
            )
        return self.notification_service.list_notifications(user_id=user.id)

    def list(self, request: Request) -> Response:
        queryset = self.get_queryset()
        # Pagination can be handled by standard DRF PageNumberPagination if configured globally
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return success_response(
            data=serializer.data, message="Notifications retrieved."
        )

    def retrieve(self, request: Request, pk: str = None) -> Response:
        notification = self.notification_service.get_notification(notification_id=pk)
        # Check permissions explicitly
        if notification.user != request.user:
            self.permission_denied(
                request, message="You do not have permission to perform this action."
            )

        serializer = self.get_serializer(notification)
        return success_response(
            data=serializer.data, message="Notification retrieved successfully."
        )

    @action(detail=True, methods=["post"])
    def mark_read(self, request: Request, pk: str = None) -> Response:
        notification = self.notification_service.get_notification(notification_id=pk)
        if notification.user != request.user:
            self.permission_denied(
                request, message="You do not have permission to perform this action."
            )

        updated_notification = self.notification_service.mark_as_read(
            notification_id=pk
        )
        return success_response(
            data=NotificationSerializer(updated_notification).data,
            message="Notification marked as read.",
        )

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request: Request) -> Response:
        notifications = self.get_queryset().filter(is_read=False)
        for notif in notifications:
            notif.mark_as_read()
        return success_response(data={}, message="All notifications marked as read.")

    def destroy(self, request: Request, pk: str = None) -> Response:
        notification = self.notification_service.get_notification(notification_id=pk)
        if notification.user != request.user:
            self.permission_denied(
                request, message="You do not have permission to perform this action."
            )

        self.notification_service.delete_notification(notification_id=pk)
        return success_response(
            data={},
            message="Notification deleted successfully.",
            status_code=status.HTTP_200_OK,
        )
