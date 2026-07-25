"""
Unit and integration tests for User Login, Logout, JWT Rotation, and Blacklisting.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from modules.users.models.user import User


class LoginLogoutAPITests(APITestCase):
    """Test suite for `/api/v1/auth/login/`, `/logout/`, and `/refresh/` endpoints."""

    def setUp(self) -> None:
        self.login_url = reverse("authentication:login")
        self.logout_url = reverse("authentication:logout")
        self.refresh_url = reverse("authentication:refresh")

        self.password = "SecurePassword456!"
        self.user = User.objects.create_user(
            email="scientist.anita@dhatree.ai",
            username="anita_scientist",
            password=self.password,
            role=User.Role.RESEARCHER,
        )

    def test_successful_login_with_email(self):
        """Verify login via email returns valid JWT tokens and profile representation."""
        response = self.client.post(
            self.login_url,
            {"identifier": "scientist.anita@dhatree.ai", "password": self.password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertIn("tokens", response.data["data"])
        self.assertIn("access", response.data["data"]["tokens"])
        self.assertIn("refresh", response.data["data"]["tokens"])

    def test_successful_login_with_username(self):
        """Verify login via username returns valid JWT tokens."""
        response = self.client.post(
            self.login_url,
            {"identifier": "anita_scientist", "password": self.password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])

    def test_login_with_wrong_password_fails(self):
        """Verify incorrect credentials return 401 Unauthorized with standardized error payload."""
        response = self.client.post(
            self.login_url,
            {"identifier": "scientist.anita@dhatree.ai", "password": "WrongPassword!"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data["success"])
        self.assertEqual(
            response.data["message"], "Invalid email/username or password."
        )

    def test_login_on_soft_deleted_account_fails(self):
        """Verify login attempt on soft-deleted profile is rejected with 401 Unauthorized."""
        self.user.soft_delete()
        response = self.client.post(
            self.login_url,
            {"identifier": "scientist.anita@dhatree.ai", "password": self.password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data["success"])

    def test_login_on_suspended_account_fails(self):
        """Verify login attempt on suspended profile returns 403 Forbidden."""
        self.user.account_status = User.AccountStatus.SUSPENDED
        self.user.save()
        response = self.client.post(
            self.login_url,
            {"identifier": "scientist.anita@dhatree.ai", "password": self.password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data["success"])

    def test_refresh_token_rotation_and_logout_blacklisting(self):
        """Verify refresh token rotation and token blacklisting on logout."""
        # Step 1: Login to get refresh token
        login_resp = self.client.post(
            self.login_url,
            {"identifier": "anita_scientist", "password": self.password},
            format="json",
        )
        refresh_token = login_resp.data["data"]["tokens"]["refresh"]

        # Step 2: Refresh token pair
        refresh_resp = self.client.post(
            self.refresh_url, {"refresh": refresh_token}, format="json"
        )
        self.assertEqual(refresh_resp.status_code, status.HTTP_200_OK)
        new_refresh_token = refresh_resp.data["data"]["refresh"]

        # Step 3: Logout using the latest refresh token
        logout_resp = self.client.post(
            self.logout_url, {"refresh": new_refresh_token}, format="json"
        )
        self.assertEqual(logout_resp.status_code, status.HTTP_200_OK)
        self.assertTrue(logout_resp.data["success"])

        # Step 4: Attempt to refresh using the blacklisted token must fail with 400 or 401
        failed_refresh = self.client.post(
            self.refresh_url, {"refresh": new_refresh_token}, format="json"
        )
        self.assertIn(
            failed_refresh.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED],
        )
        self.assertFalse(failed_refresh.data["success"])
