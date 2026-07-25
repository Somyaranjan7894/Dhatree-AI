import os
import sys
import time
import json
from pathlib import Path

# Setup Django Environment
project_root = Path(__file__).resolve().parent.parent.parent
backend_dir = project_root / "backend"
sys.path.append(str(backend_dir))
sys.path.append(str(project_root)) # Required for ai.disease_detection imports
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
import django
django.setup()

from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile

def main():
    print("Starting Backend Validation...")
    reports_dir = project_root / "ai" / "reports" / "disease_detection_phase20"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    client = Client()
    
    # We need a sample image
    data_dir = project_root / "ai" / "datasets" / "raw" / "plantvillage"
    # Find any image
    sample_img = None
    for ext in ['*.jpg', '*.JPG', '*.png', '*.PNG', '*.jpeg', '*.JPEG']:
        files = list(data_dir.rglob(ext))
        if files:
            sample_img = files[0]
            break
            
    if not sample_img:
        print("No sample image found.")
        return
        
    print(f"Testing with sample image: {sample_img}")
    
    with open(sample_img, 'rb') as f:
        img_data = f.read()
        
    img_file = SimpleUploadedFile(name='test_image.jpg', content=img_data, content_type='image/jpeg')
    
    start_time = time.time()
    
    # The endpoint might be /api/disease/predict or similar. Let's try some common ones
    # or we can test the service function directly if we don't know the URL.
    try:
        from modules.disease_detection.services.prediction_service import DiseasePredictionService
        print("Testing via DiseasePredictionService._run_inference directly...")
        service = DiseasePredictionService()
        
        # Test requires absolute path of image
        predicted_class, confidence, metadata = service._run_inference(str(sample_img))
        
        end_time = time.time()
        
        print("Service Result:")
        print(f"Predicted: {predicted_class}, Confidence: {confidence}")
        
        backend_metrics = {
            "Time Taken (s)": end_time - start_time,
            "Success": predicted_class not in ["Model Not Found", "Inference Error", "System Error"],
            "Top Prediction": predicted_class,
            "Confidence": confidence,
            "Metadata": metadata
        }
        
    except Exception as e:
        print(f"Error testing service directly: {e}")
        import traceback
        traceback.print_exc()
        backend_metrics = {
            "Success": False,
            "Error": str(e)
        }
        
    with open(reports_dir / "backend_validation.json", "w") as f:
        json.dump(backend_metrics, f, indent=4)
        
    print("Backend validation completed.")

if __name__ == "__main__":
    main()
