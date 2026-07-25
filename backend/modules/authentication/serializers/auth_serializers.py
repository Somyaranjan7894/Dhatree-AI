"""
Input and validation serializers for authentication workflows.
Enforces strict credential validation and password strength rules before invoking AuthService.
"""

import re

from rest_framework import serializers

from modules.users.models.user import User


class RegisterSerializer(serializers.Serializer):
    """Input serializer for user account registration."""

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, write_only=True, min_length=8)
    password_confirm = serializers.CharField(required=True, write_only=True)
    full_name = serializers.CharField(required=False, allow_blank=True, max_length=255)
    phone_number = serializers.CharField(
        required=False, allow_blank=True, max_length=20
    )
    role = serializers.ChoiceField(choices=User.Role.choices, default=User.Role.FARMER)

    def validate_email(self, value: str) -> str:
        return value.strip().lower()

    def validate_username(self, value: str) -> str:
        clean_name = value.strip()
        if not re.match(r"^[\w.@+-]+$", clean_name):
            raise serializers.ValidationError(
                "Username may only contain letters, numbers, and @/./+/-/_ characters."
            )
        return clean_name

    def validate(self, attrs: dict) -> dict:
        if attrs.get("password") != attrs.get("password_confirm"):
            raise serializers.ValidationError(
                {"password_confirm": "The two password fields didn't match."}
            )

        password = attrs.get("password")
        if (
            not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"[0-9]", password)
        ):
            raise serializers.ValidationError(
                {
                    "password": "Password must contain at least one uppercase letter, one lowercase letter, and one digit."
                }
            )
        return attrs


class LoginSerializer(serializers.Serializer):
    """Input serializer for authentication credentials."""

    identifier = serializers.CharField(
        required=True, help_text="Email address or username."
    )
    password = serializers.CharField(required=True, write_only=True)

    def validate_identifier(self, value: str) -> str:
        return value.strip()


class LogoutSerializer(serializers.Serializer):
    """Input serializer for JWT refresh token blacklisting upon logout."""

    refresh = serializers.CharField(
        required=True, help_text="Refresh token to blacklist."
    )


class RefreshTokenSerializer(serializers.Serializer):
    """Input serializer for rotating an access/refresh token pair."""

    refresh = serializers.CharField(required=True, help_text="Valid refresh token.")


class ChangePasswordSerializer(serializers.Serializer):
    """Input serializer for updating an authenticated user's password."""

    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: dict) -> dict:
        if attrs.get("new_password") != attrs.get("new_password_confirm"):
            raise serializers.ValidationError(
                {"new_password_confirm": "The new password fields didn't match."}
            )
        if attrs.get("old_password") == attrs.get("new_password"):
            raise serializers.ValidationError(
                {
                    "new_password": "New password cannot be identical to your old password."
                }
            )

        password = attrs.get("new_password")
        if (
            not re.search(r"[A-Z]", password)
            or not re.search(r"[a-z]", password)
            or not re.search(r"[0-9]", password)
        ):
            raise serializers.ValidationError(
                {
                    "new_password": "Password must contain at least one uppercase letter, one lowercase letter, and one digit."
                }
            )
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    """Input serializer to initiate password reset via email."""

    email = serializers.EmailField(required=True)

    def validate_email(self, value: str) -> str:
        return value.strip().lower()


class ResetPasswordSerializer(serializers.Serializer):
    """Input serializer to finalize password reset using verification token."""

    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=8)
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs: dict) -> dict:
        if attrs.get("new_password") != attrs.get("new_password_confirm"):
            raise serializers.ValidationError(
                {"new_password_confirm": "The new password fields didn't match."}
            )
        return attrs


class VerifyEmailSerializer(serializers.Serializer):
    """Input serializer to verify user account email verification token."""

    token = serializers.CharField(required=True)
