import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import get_user_model
User = get_user_model()
from modules.disease_detection.models.prediction import DiseasePrediction
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    return User.objects.create_user(username="testuser", email="test@example.com", password="password123")

@pytest.mark.django_db
def test_prediction_creation_and_history(api_client, test_user):
    # Authenticate
    api_client.force_authenticate(user=test_user)
    
    # 1. Create a valid dummy image
    image_content = (
        b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
        b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
        b'\x02\x4c\x01\x00\x3b'
    )
    image = SimpleUploadedFile("test_leaf.gif", image_content, content_type="image/gif")
    
    # 2. Predict (POST) with mock
    from unittest.mock import patch
    
    mock_metadata = {
        "top_predictions": [{"class": "Apple___healthy", "confidence": 0.99}],
        "heatmap_base64": "mock_base64"
    }
    
    with patch('modules.disease_detection.services.prediction_service.DiseasePredictionService._run_inference') as mock_inference:
        mock_inference.return_value = ("Apple___healthy", 0.99, mock_metadata)
        
        url = reverse("disease_detection:disease-prediction-list")
        response = api_client.post(url, {"image": image}, format="multipart")
    
    # Assert successful creation
    assert response.status_code == 201
    
    # Assert fields are returned
    data = response.json()
    assert "id" in data
    assert "predicted_class" in data
    assert "confidence_score" in data
    
    # Since we use the mock inference, it should be one of our hardcoded choices
    assert data["predicted_class"] != "Processing..."
    assert data["confidence_score"] > 0.0
    
    # 3. Fetch History (GET)
    response_history = api_client.get(url)
    assert response_history.status_code == 200
    
    history_data = response_history.json()
    # Check if the list contains our new prediction
    assert isinstance(history_data, list) or "data" in history_data
    items = history_data if isinstance(history_data, list) else history_data["data"]
    assert len(items) == 1
    assert items[0]["id"] == data["id"]
