import os
from pathlib import Path
from PIL import Image
import numpy as np
import json
import datetime

# The 38 classes of the PlantVillage dataset
PLANT_VILLAGE_CLASSES = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
    "Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)___Common_rust_", 
    "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy", "Grape___Black_rot", 
    "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot", "Peach___healthy",
    "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy", "Potato___Early_blight", 
    "Potato___Late_blight", "Potato___healthy", "Raspberry___healthy", "Soybean___healthy",
    "Squash___Powdery_mildew", "Strawberry___Leaf_scorch", "Strawberry___healthy",
    "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight", 
    "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot", "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus", 
    "Tomato___healthy"
]

def generate_mock_dataset():
    raw_dir = Path("ai/datasets/raw/plantvillage")
    metadata_dir = Path("ai/datasets/metadata")
    
    metadata_dir.mkdir(parents=True, exist_ok=True)
    
    if raw_dir.exists():
        classes_present = [d for d in raw_dir.iterdir() if d.is_dir()]
        if len(classes_present) == 38:
            print("Dataset appears to already be generated.")
            return
            
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating mock PlantVillage dataset for {len(PLANT_VILLAGE_CLASSES)} classes...")
    
    images_per_class = 5 # Tiny subset for validation
    
    for c_name in PLANT_VILLAGE_CLASSES:
        class_dir = raw_dir / c_name
        class_dir.mkdir(exist_ok=True)
        
        for i in range(images_per_class):
            # Generate a solid color or random noise image to simulate an actual image
            img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
            img = Image.fromarray(img_array)
            img.save(class_dir / f"img_{i}.jpg")
            
    print("Export complete.")
    
    # Save metadata
    metadata = {
        "dataset": "plant_village_mock",
        "downloaded_at": datetime.datetime.now().isoformat(),
        "num_classes": len(PLANT_VILLAGE_CLASSES),
        "total_images": len(PLANT_VILLAGE_CLASSES) * images_per_class,
        "source": "generated_mock_due_to_403"
    }
    with open(metadata_dir / "dataset_version.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
if __name__ == "__main__":
    generate_mock_dataset()
