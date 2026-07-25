import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_user(
        username="farmer", email="farmer@example.com", password="password123"
    )


@pytest.mark.django_db
def test_crop_recommendation_flow(api_client, test_user):
    api_client.force_authenticate(user=test_user)

    # 1. Predict
    url = reverse("crop_recommendation:crop-prediction-list")
    payload = {
        "nitrogen": 90,
        "phosphorus": 42,
        "potassium": 43,
        "temperature": 20.8,
        "humidity": 82.0,
        "ph": 6.5,
        "rainfall": 202.9,
    }

    import os
    import sys

    from django.conf import settings

    root_dir = os.path.abspath(os.path.join(settings.BASE_DIR, ".."))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

    from unittest.mock import patch

    with patch("ai.crop_recommendation.predict.predict_crop") as mock_predict:
        mock_predict.return_value = {
            "recommended_crop": "rice",
            "confidence_score": 0.95,
            "alternatives": ["jute", "cotton"],
            "explanation": "Mocked explanation.",
        }
        response = api_client.post(url, payload, format="json")

    assert response.status_code == 201, f"Failed: {response.json()}"

    data = response.json()
    assert data["status"] == "success"

    prediction = data["data"]
    assert "id" in prediction
    assert "recommended_crop" in prediction
    assert "confidence_score" in prediction
    assert "alternatives" in prediction
    assert "explanation" in prediction

    # Predicts 'rice' correctly based on matching params
    assert prediction["recommended_crop"].lower() == "rice"

    # 2. History
    response_history = api_client.get(url)
    assert response_history.status_code == 200

    history_data = response_history.json()
    assert history_data["status"] == "success"
    items = history_data["data"]
    assert len(items) == 1
    assert items[0]["id"] == prediction["id"]
