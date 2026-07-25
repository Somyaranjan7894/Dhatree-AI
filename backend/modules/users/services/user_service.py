"""
UserService orchestrating profile retrieval, updates, and account management.
Decouples views from UserRepository and enforces business invariants.
"""
from typing import Any, Dict, Optional
from django.db.models.query import QuerySet
from core.exceptions import ResourceNotFoundError, ValidationError
from core.services.base import BaseService
from modules.users.models.user import User
from modules.users.repositories.user_repository import UserRepository


class UserService(BaseService):
    """Business service for User profile and account lifecycle management."""

    def __init__(self, user_repository: Optional[UserRepository] = None) -> None:
        super().__init__()
        self.user_repo = user_repository or UserRepository()

    def get_user_profile(self, user_id: Any) -> User:
        """Retrieve a user profile by ID or raise ResourceNotFoundError."""
        self.log_operation("get_user_profile", {"user_id": str(user_id)})
        return self.user_repo.get_by_id_or_raise(user_id)

    def list_users(self, **filters: Any) -> QuerySet[User]:
        """List active platform users with optional filters."""
        self.log_operation("list_users", filters)
        return self.user_repo.list_all(**filters)

    def update_user_profile(self, user_id: Any, **update_data: Any) -> User:
        """
        Update user profile fields after verifying uniqueness constraints on email and username.
        """
        self.log_operation("update_user_profile", {"user_id": str(user_id), "fields": list(update_data.keys())})
        user = self.user_repo.get_by_id_or_raise(user_id)

        email = update_data.get("email")
        if email and email.strip() != user.email:
            if self.user_repo.check_email_exists(email, exclude_user_id=user.id):
                raise ValidationError("That email address is already taken by another account.")

        username = update_data.get("username")
        if username and username.strip() != user.username:
            if self.user_repo.check_username_exists(username, exclude_user_id=user.id):
                raise ValidationError("That username is already taken by another account.")

        # Prevent direct privilege escalation or account status manipulation through profile update
        update_data.pop("role", None)
        update_data.pop("account_status", None)
        update_data.pop("is_verified", None)
        update_data.pop("is_deleted", None)
        update_data.pop("password", None)

        return self.user_repo.update(user, **update_data)

    def soft_delete_user_account(self, user_id: Any) -> None:
        """Soft-delete a user profile and deactivate their account."""
        self.log_operation("soft_delete_user_account", {"user_id": str(user_id)})
        user = self.user_repo.get_by_id_or_raise(user_id)
        self.user_repo.soft_delete(user)
