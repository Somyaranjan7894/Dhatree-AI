import os
import sys
import django
import json
from django.core.files.uploadedfile import SimpleUploadedFile

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()
from django.conf import settings
sys.path.insert(0, os.path.abspath(os.path.join(settings.BASE_DIR, '..')))
from django.contrib.auth import get_user_model
User = get_user_model()

def audit_ai_models():
    print("--- AI Model Audit ---")
    
    try:
        from ai_engine.models_registry.registry import ModelsRegistry
        registry = ModelsRegistry()
    except Exception as e:
        print(f"[FAIL] Registry Initialization: {e}")
        return

    # Create dummy user
    user, _ = User.objects.get_or_create(email="audit_ai@example.com", username="audit_ai")

    # 1. Crop Recommendation
    print("Testing Crop Recommendation...")
    try:
        from modules.crop_recommendation.services.recommendation_service import CropRecommendationService
        service = CropRecommendationService()
        data = {
            "nitrogen": 90, "phosphorus": 42, "potassium": 43,
            "temperature": 20.8, "humidity": 82.0, "ph": 6.5, "rainfall": 202.9
        }
        result = service.predict_crop(user=user, data=data)
        print(f"[OK] Crop Recommendation: {result.recommended_crop}")
    except Exception as e:
        print(f"[FAIL] Crop Recommendation: {e}")

    # 2. Fertilizer Recommendation
    print("Testing Fertilizer Recommendation...")
    try:
        from modules.fertilizer_recommendation.services.recommendation_service import FertilizerRecommendationService
        service = FertilizerRecommendationService()
        data = {
            "temperature": 26.0, "humidity": 52.0, "moisture": 38.0,
            "soil_type": "Sandy", "crop_type": "Maize",
            "nitrogen": 37, "potassium": 0, "phosphorus": 0,
            "ph_level": 6.5, "rainfall": 200.0
        }
        result = service.predict_fertilizer(user=user, data=data)
        print(f"[OK] Fertilizer Recommendation: {result.recommended_fertilizer}")
    except Exception as e:
        print(f"[FAIL] Fertilizer Recommendation: {e}")

    # 3. Disease Detection
    print("Testing Disease Detection...")
    try:
        from modules.disease_detection.services.prediction_service import DiseasePredictionService
        service = DiseasePredictionService()
        from PIL import Image
        import io
        img = Image.new('RGB', (224, 224), color = (73, 109, 137))
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        uploaded_file = SimpleUploadedFile("test.jpg", img_bytes.getvalue(), content_type="image/jpeg")
        result = service.predict_disease(user=user, image_file=uploaded_file)
        print(f"[OK] Disease Detection: {result.predicted_class}")
    except Exception as e:
        print(f"[FAIL] Disease Detection: {e}")

    # 4. Disease Diagnosis
    print("Testing Disease Diagnosis...")
    try:
        from modules.disease_diagnosis.models.knowledge import Disease
        disease = Disease.objects.first()
        if disease:
            print(f"[OK] Disease Diagnosis retrieved for '{disease.name}'.")
        else:
            print(f"[OK] Disease Diagnosis table is empty (but model works).")
    except Exception as e:
        print(f"[FAIL] Disease Diagnosis: {e}")

if __name__ == "__main__":
    audit_ai_models()


