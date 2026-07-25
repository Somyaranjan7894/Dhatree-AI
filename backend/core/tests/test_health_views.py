import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestHealthViews:
    def setup_method(self):
        self.client = APIClient()

    def test_liveness_endpoint(self):
        url = reverse("liveness")
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["status"] == "ok"

    def test_readiness_endpoint(self):
        url = reverse("readiness")
        response = self.client.get(url)
        # Database connection should be ok in test environment
        assert response.status_code == 200
        assert response.data["status"] == "ok"
        assert response.data["database"] == "ok"
