"""
Unit and integration tests for User management endpoints and RBAC constraints.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from modules.users.models.user import User


class UserManagementAPITests(APITestCase):
    """Test suite for `/api/v1/users/` and `/api/v1/auth/me/` endpoints."""

    def setUp(self) -> None:
        self.password = "SecureAdmin123!"
        self.admin_user = User.objects.create_superuser(
            email="admin.suresh@dhatree.ai",
            username="admin_suresh",
            password=self.password,
        )
        self.farmer_user = User.objects.create_user(
            email="farmer.gopal@dhatree.ai",
            username="farmer_gopal",
            password=self.password,
            role=User.Role.FARMER,
            full_name="Gopal Rao",
        )
        self.list_url = reverse("users:user-list")
        self.detail_url = reverse(
            "users:user-detail", kwargs={"pk": self.farmer_user.pk}
        )
        self.me_url = reverse("authentication:me")

    def test_list_users_admin_only(self):
        """Verify only platform administrators can list all users."""
        # Anonymous
        response_anon = self.client.get(self.list_url)
        self.assertEqual(response_anon.status_code, status.HTTP_401_UNAUTHORIZED)

        # Farmer
        self.client.force_authenticate(user=self.farmer_user)
        response_farmer = self.client.get(self.list_url)
        self.assertEqual(response_farmer.status_code, status.HTTP_403_FORBIDDEN)

        # Admin
        self.client.force_authenticate(user=self.admin_user)
        response_admin = self.client.get(self.list_url)
        self.assertEqual(response_admin.status_code, status.HTTP_200_OK)
        self.assertTrue(response_admin.data["success"])

    def test_retrieve_current_user_me(self):
        """Verify `/api/v1/auth/me/` returns accurate details for authenticated user."""
        self.client.force_authenticate(user=self.farmer_user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["email"], self.farmer_user.email)
        self.assertEqual(response.data["data"]["role"], User.Role.FARMER)

    def test_update_profile_prevents_privilege_escalation(self):
        """Verify profile updates cannot alter role, verification status, or active flags."""
        self.client.force_authenticate(user=self.farmer_user)
        update_data = {
            "full_name": "Gopal Rao Updated",
            "phone_number": "+918888888888",
            "role": "admin",  # Attempt privilege escalation
            "is_verified": True,  # Attempt self verification
        }
        response = self.client.patch(self.detail_url, update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["full_name"], "Gopal Rao Updated")

        self.farmer_user.refresh_from_db()
        self.assertEqual(self.farmer_user.role, User.Role.FARMER)
        self.assertFalse(self.farmer_user.is_verified)

    def test_soft_delete_user_account_by_admin(self):
        """Verify admin can soft-delete a user account without scrubbing database history."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])

        # Verify user is excluded from active_objects and marked as deleted
        self.assertFalse(User.active_objects.filter(pk=self.farmer_user.pk).exists())
        self.assertTrue(User.objects.filter(pk=self.farmer_user.pk).exists())

        soft_deleted_user = User.objects.get(pk=self.farmer_user.pk)
        self.assertTrue(soft_deleted_user.is_deleted)
        self.assertFalse(soft_deleted_user.is_active)
        self.assertIsNotNone(soft_deleted_user.deleted_at)
