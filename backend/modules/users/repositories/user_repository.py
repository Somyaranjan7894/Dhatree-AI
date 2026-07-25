"""
UserRepository encapsulating all database queries and transactions for the User domain boundary.
Prevents direct ORM calls from Services or Views.
"""
from typing import Any, Optional, Type
from django.db.models import Q
from core.repositories.base import BaseRepository
from modules.users.models.user import User


class UserRepository(BaseRepository[User]):
    """Data access repository for User entities."""

    @property
    def model_class(self) -> Type[User]:
        return User

    def get_by_id(self, entity_id: Any) -> Optional[User]:
        """Retrieve a user by ID using `active_objects` to exclude soft deleted users."""
        try:
            return self.model_class.active_objects.get(pk=entity_id)
        except self.model_class.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve an active user by normalized email address."""
        if not email:
            return None
        try:
            return self.model_class.active_objects.get(email__iexact=email.strip())
        except self.model_class.DoesNotExist:
            return None

    def get_by_username(self, username: str) -> Optional[User]:
        """Retrieve an active user by username."""
        if not username:
            return None
        try:
            return self.model_class.active_objects.get(username__iexact=username.strip())
        except self.model_class.DoesNotExist:
            return None

    def get_by_email_or_username(self, identifier: str) -> Optional[User]:
        """Retrieve an active user by either email or username."""
        if not identifier:
            return None
        clean_id = identifier.strip()
        try:
            return self.model_class.active_objects.get(
                Q(email__iexact=clean_id) | Q(username__iexact=clean_id)
            )
        except self.model_class.DoesNotExist:
            return None

    def check_email_exists(self, email: str, exclude_user_id: Optional[Any] = None) -> bool:
        """Check if an email address is already taken by any user."""
        if not email:
            return False
        qs = self.model_class.objects.filter(email__iexact=email.strip())
        if exclude_user_id:
            qs = qs.exclude(pk=exclude_user_id)
        return qs.exists()

    def check_username_exists(self, username: str, exclude_user_id: Optional[Any] = None) -> bool:
        """Check if a username is already taken by any user."""
        if not username:
            return False
        qs = self.model_class.objects.filter(username__iexact=username.strip())
        if exclude_user_id:
            qs = qs.exclude(pk=exclude_user_id)
        return qs.exists()

    def create_user_with_password(self, email: str, username: str, password: str, **extra_fields: Any) -> User:
        """Create a user profile with hashed credentials via custom UserManager."""
        return self.model_class.objects.create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields,
        )

    def soft_delete(self, user: User) -> None:
        """Execute soft deletion on a user account."""
        user.soft_delete()
