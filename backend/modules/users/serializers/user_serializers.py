"""
Serializers for User profile representation and modification.
"""
from rest_framework import serializers
from modules.users.models.user import User


class UserSerializer(serializers.ModelSerializer):
    """Read-only representation of a user profile."""

    role_display = serializers.CharField(source="get_role_display", read_only=True)
    status_display = serializers.CharField(source="get_account_status_display", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "full_name",
            "phone_number",
            "profile_photo",
            "role",
            "role_display",
            "account_status",
            "status_display",
            "is_verified",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields


class UserUpdateSerializer(serializers.ModelSerializer):
    """Input serializer for updating user profile attributes."""

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "full_name",
            "phone_number",
            "profile_photo",
        ]

    def validate_email(self, value: str) -> str:
        return value.strip().lower()

    def validate_username(self, value: str) -> str:
        return value.strip()
