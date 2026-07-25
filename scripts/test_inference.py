import os
import sys
import django
import random
from pathlib import Path

# Setup Django environment
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from ai_engine.pipelines.disease_detection.pipeline import DiseaseDetectionPipeline

def test_inference():
    print("Testing Disease Detection Pipeline using real PlantVillage images...")
    
    base_dir = Path(__file__).resolve().parent.parent
    dataset_dir = base_dir / "ai" / "datasets" / "raw" / "plantvillage"
    
    if not dataset_dir.exists():
        print("Dataset directory not found!")
        sys.exit(1)
        
    pipeline = DiseaseDetectionPipeline()
    if pipeline.model is None:
        print("Failed to load the model from registry.")
        sys.exit(1)
        
    print("Model loaded successfully via ModelsRegistry.\n")
    
    classes = sorted([d for d in os.listdir(dataset_dir) if (dataset_dir / d).is_dir()])
    
    # Pick 50 random test images across classes
    import time
    
    test_images = []
    for cls in classes:
        class_path = dataset_dir / cls
        images = [f for f in os.listdir(class_path) if f.lower().endswith('.jpg')]
        for img in images[:2]: # Grab a couple from each class to get to ~50
            test_images.append((cls, class_path / img))
            if len(test_images) >= 50:
                break
        if len(test_images) >= 50:
            break
            
    success_count = 0
    total = 0
    inference_times = []
    
    for cls, img_file in test_images:
        with open(img_file, "rb") as f:
            img_bytes = f.read()
            
        try:
            start_t = time.time()
            processed = pipeline.preprocess_image(img_bytes)
            pred = pipeline.analyze(processed)
            infer_t = time.time() - start_t
            inference_times.append(infer_t)
            
            print(f"--- Testing Image from class: {cls} ---")
            print(f"Prediction Status: {pred['status']}")
            
            analysis = pred['analysis']
            print(f"Predicted Class: {analysis.get('predicted_class', analysis.get('disease', 'Unknown'))}")
            print(f"Confidence: {analysis.get('confidence', 0.0):.4f}")
            if 'top_predictions' in analysis:
                print("Top 3 Predictions:")
                for p in analysis['top_predictions']:
                    print(f"  - {p['class']}: {p['confidence']:.4f}")
            elif 'probabilities' in analysis:
                probs = analysis['probabilities']
                top_3 = sorted(probs.items(), key=lambda item: item[1], reverse=True)[:3]
                print("Top 3 Predictions:")
                for k, v in top_3:
                    print(f"  - {k}: {v:.4f}")
            
            print()
            success_count += 1
            total += 1
        except Exception as e:
            print(f"Error analyzing {img_file}: {e}")
            total += 1
            
    avg_time = sum(inference_times) / len(inference_times) if inference_times else 0
    print(f"Inference test completed: {success_count}/{total} successful.")
    print(f"Average Inference Time per image: {avg_time:.4f} seconds")
    
if __name__ == "__main__":
    test_inference()
