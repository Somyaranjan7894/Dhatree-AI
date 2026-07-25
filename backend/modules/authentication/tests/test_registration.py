"""
Unit and integration tests for User Registration workflow and validation rules.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from modules.users.models.user import User


class RegistrationAPITests(APITestCase):
    """Test suite for `/api/v1/auth/register/` endpoint."""

    def setUp(self) -> None:
        self.register_url = reverse("authentication:register")
        self.valid_payload = {
            "email": "farmer.ramesh@dhatree.ai",
            "username": "farmer_ramesh",
            "password": "StrongPassword123!",
            "password_confirm": "StrongPassword123!",
            "full_name": "Ramesh Kumar",
            "phone_number": "+919876543210",
            "role": "farmer",
        }

    def test_successful_registration(self):
        """Verify valid registration creates user and returns JWT tokens with standardized format."""
        response = self.client.post(
            self.register_url, self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(
            response.data["message"], "User account registered successfully."
        )
        self.assertIn("user", response.data["data"])
        self.assertIn("tokens", response.data["data"])
        self.assertIn("access", response.data["data"]["tokens"])
        self.assertIn("refresh", response.data["data"]["tokens"])

        user = User.objects.get(email="farmer.ramesh@dhatree.ai")
        self.assertEqual(user.username, "farmer_ramesh")
        self.assertEqual(user.role, User.Role.FARMER)
        self.assertTrue(user.check_password("StrongPassword123!"))

    def test_duplicate_email_registration_fails(self):
        """Verify registration with duplicate email fails cleanly with 400 and JSON error payload."""
        User.objects.create_user(
            email="farmer.ramesh@dhatree.ai",
            username="existing_user",
            password="OtherPassword123!",
        )
        response = self.client.post(
            self.register_url, self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertIn("errors", response.data)
        self.assertIn("email", response.data["errors"])

    def test_duplicate_username_registration_fails(self):
        """Verify registration with duplicate username fails cleanly with 400 and JSON error payload."""
        User.objects.create_user(
            email="other.email@dhatree.ai",
            username="farmer_ramesh",
            password="OtherPassword123!",
        )
        response = self.client.post(
            self.register_url, self.valid_payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertIn("errors", response.data)
        self.assertIn("username", response.data["errors"])

    def test_password_mismatch_fails(self):
        """Verify mismatched password and confirmation fail validation."""
        payload = self.valid_payload.copy()
        payload["password_confirm"] = "DifferentPassword123!"
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertIn("password_confirm", response.data["errors"])

    def test_weak_password_fails(self):
        """Verify password without numbers/uppercase/lowercase fails validation."""
        payload = self.valid_payload.copy()
        payload["password"] = "alllowercase"
        payload["password_confirm"] = "alllowercase"
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertIn("password", response.data["errors"])
