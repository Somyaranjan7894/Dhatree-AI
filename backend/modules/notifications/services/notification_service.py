"""
Notification Service.
"""

from django.db import transaction

from core.services.base import BaseService
from modules.notifications.models.notification import Notification
from modules.notifications.repositories.notification_repository import (
    NotificationRepository,
)


class NotificationService(BaseService):
    def __init__(self):
        super().__init__()
        self.notification_repository = NotificationRepository()

    def get_notification(self, notification_id: str) -> Notification:
        return self.notification_repository.get_by_id_or_raise(notification_id)

    def list_notifications(self, user_id: str):
        return self.notification_repository.list_active_for_user(user_id=user_id)

    @transaction.atomic
    def create_notification(self, user_id: str, **data) -> Notification:
        data["user_id"] = user_id
        self.log_operation("create_notification", {"user_id": user_id})
        return self.notification_repository.create(**data)

    @transaction.atomic
    def mark_as_read(self, notification_id: str) -> Notification:
        notification = self.get_notification(notification_id)
        self.log_operation(
            "mark_notification_as_read", {"notification_id": notification_id}
        )
        notification.mark_as_read()
        return notification

    @transaction.atomic
    def delete_notification(self, notification_id: str) -> None:
        notification = self.get_notification(notification_id)
        self.log_operation("delete_notification", {"notification_id": notification_id})
        notification.soft_delete()
