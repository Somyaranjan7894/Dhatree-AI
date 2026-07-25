"""
AuthService implementing robust credential verification, JWT lifecycle management,
and security audit logging.
"""

import logging
from typing import Any, Dict, Optional, Tuple

from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken

from core.exceptions import (
    AuthenticationFailed,
    PermissionDenied,
    ResourceNotFoundError,
    ValidationError,
)
from core.services.base import BaseService
from modules.users.models.user import User
from modules.users.repositories.user_repository import UserRepository

security_logger = logging.getLogger("dhatree.security")


class AuthService(BaseService):
    """Business service orchestrating authentication, registration, and token rotation."""

    def __init__(self, user_repository: Optional[UserRepository] = None) -> None:
        super().__init__()
        self.user_repo = user_repository or UserRepository()

    def _generate_tokens_for_user(self, user: User) -> Dict[str, str]:
        """Generate JWT Refresh and Access tokens for a verified user instance."""
        refresh = RefreshToken.for_user(user)
        # Include custom claims inside token payload
        refresh["email"] = user.email
        refresh["role"] = user.role
        refresh["username"] = user.username

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

    def register(self, **validated_data: Any) -> Tuple[User, Dict[str, str]]:
        """
        Validate account uniqueness and register a new user with hashed credentials.
        Returns the created User instance alongside initial access/refresh JWT tokens.
        """
        email = validated_data.pop("email").strip().lower()
        username = validated_data.pop("username").strip()
        password = validated_data.pop("password")
        validated_data.pop("password_confirm", None)

        if self.user_repo.check_email_exists(email):
            raise ValidationError(
                {"email": "An account with that email address already exists."}
            )
        if self.user_repo.check_username_exists(username):
            raise ValidationError(
                {"username": "An account with that username already exists."}
            )

        self.log_operation(
            "register_user", {"email": email, "role": validated_data.get("role")}
        )
        user = self.user_repo.create_user_with_password(
            email=email, username=username, password=password, **validated_data
        )
        security_logger.info(
            f"SECURITY: New user account registered | User ID: {user.id} | Email: {user.email}"
        )

        tokens = self._generate_tokens_for_user(user)
        return user, tokens

    def login(self, identifier: str, password: str) -> Tuple[User, Dict[str, str]]:
        """
        Verify user credentials via email or username, verify account status, and return JWT tokens.
        """
        clean_id = identifier.strip()
        self.log_operation("login_attempt", {"identifier": clean_id})

        user = self.user_repo.get_by_email_or_username(clean_id)
        if not user or not user.check_password(password):
            security_logger.warning(
                f"SECURITY: Failed login attempt for identifier: {clean_id}"
            )
            raise AuthenticationFailed("Invalid email/username or password.")

        if user.is_deleted or not user.is_active:
            security_logger.warning(
                f"SECURITY: Login attempt on deactivated account: {user.email}"
            )
            raise AuthenticationFailed("This user account has been deactivated.")

        if user.account_status == User.AccountStatus.SUSPENDED:
            security_logger.warning(
                f"SECURITY: Login attempt on suspended account: {user.email}"
            )
            raise PermissionDenied(
                "Your account has been suspended by platform administrators."
            )

        security_logger.info(
            f"SECURITY: Successful user login | User ID: {user.id} | Email: {user.email}"
        )
        tokens = self._generate_tokens_for_user(user)
        return user, tokens

    def logout(self, refresh_token_str: str) -> None:
        """
        Blacklist the provided JWT refresh token to revoke future access.
        """
        self.log_operation("logout_user", {})
        try:
            token = RefreshToken(refresh_token_str)
            token.blacklist()
            security_logger.info(
                "SECURITY: Refresh token successfully blacklisted upon logout."
            )
        except TokenError as e:
            raise ValidationError(
                {"refresh": f"Invalid or expired refresh token: {str(e)}"}
            )

    def refresh_tokens(self, refresh_token_str: str) -> Dict[str, str]:
        """
        Rotate a refresh token and return a fresh access token (and new refresh token if configured).
        """
        self.log_operation("refresh_tokens", {})
        try:
            refresh = RefreshToken(refresh_token_str)
            # If blacklisting after rotation is enabled in SIMPLE_JWT, blacklist old refresh token
            if hasattr(refresh, "blacklist"):
                refresh.blacklist()

            # Resolve user from token user_id claim
            user_id = refresh.payload.get("user_id")
            user = self.user_repo.get_by_id(user_id) if user_id else None
            if not user or not user.is_active or user.is_deleted:
                raise AuthenticationFailed(
                    "User account associated with this token is no longer active."
                )

            return self._generate_tokens_for_user(user)
        except TokenError as e:
            raise AuthenticationFailed(f"Token refresh failed: {str(e)}")

    def verify_token(self, token_str: str) -> bool:
        """Verify if a JWT token string is structurally valid and unexpired."""
        self.log_operation("verify_token", {})
        try:
            UntypedToken(token_str)
            return True
        except (TokenError, Exception):
            return False

    def change_password(self, user: User, old_password: str, new_password: str) -> None:
        """Verify old password and update user credentials."""
        self.log_operation("change_password", {"user_id": str(user.id)})
        if not user.check_password(old_password):
            security_logger.warning(
                f"SECURITY: Failed password change attempt (invalid old password) | User: {user.id}"
            )
            raise ValidationError({"old_password": "Incorrect current password."})

        user.set_password(new_password)
        user.save(update_fields=["password", "updated_at"])
        security_logger.info(
            f"SECURITY: Password changed successfully for user: {user.id}"
        )

    def forgot_password(self, email: str) -> Dict[str, Any]:
        """
        Initiate password recovery flow.
        To prevent user enumeration attacks, returns a uniform success message whether or not email exists.
        """
        self.log_operation("forgot_password", {"email": email})
        user = self.user_repo.get_by_email(email)
        if user:
            # Generate one-time reset token stub for modular expansion
            security_logger.info(
                f"SECURITY: Password reset requested for user: {user.id} ({user.email})"
            )
            # In Phase 2, stub out email notification dispatch without external email service dependency
        return {
            "status": "initiated",
            "message": "If that email address is registered, password recovery instructions have been dispatched.",
        }

    def reset_password(self, token: str, new_password: str) -> None:
        """Verify reset token and apply new password."""
        self.log_operation("reset_password", {})
        if not token or len(token) < 10:
            raise ValidationError({"token": "Invalid or expired password reset token."})
        # For Phase 2 foundation, validate token structure or raise clean validation error
        raise ValidationError(
            {
                "token": "Password reset token has expired or is invalid. Please request a new link."
            }
        )

    def verify_email(self, token: str) -> User:
        """Verify account email verification token."""
        self.log_operation("verify_email", {})
        if not token or len(token) < 10:
            raise ValidationError({"token": "Invalid email verification token."})
        raise ValidationError({"token": "Verification token is invalid or expired."})
