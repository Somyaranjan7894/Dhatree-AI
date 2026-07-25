"""
Notification Repository.
"""

from typing import Type

from core.repositories.base import BaseRepository
from modules.notifications.models.notification import Notification


class NotificationRepository(BaseRepository[Notification]):
    @property
    def model_class(self) -> Type[Notification]:
        return Notification

    def list_active_for_user(self, user_id: str):
        return self.model_class.active_objects.filter(user_id=user_id)
