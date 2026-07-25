# Disease Detection Module

This directory contains the production-ready module for Crop Disease Detection using Transfer Learning.

## Folder Structure

```text
backend/ai_engine/disease_detection/
├── datasets/
│   ├── raw/
│   │   └── plantvillage/      # (Manual) Put the real dataset folders here
│   └── processed/             # Validation reports and processed data
├── evaluation/
│   └── evaluate_models.py     # Independent evaluation script
├── inference/
│   └── predict.py             # Reusable inference pipeline and Grad-CAM logic
├── models/
│   ├── checkpoints/           # Training weights and checkpoints
│   ├── exports/               # General export directory
│   └── logs/                  # TensorBoard logs
├── training/
│   └── train_models.py        # Production training pipeline for multiple architectures
├── utils/
│   ├── dataset_utils.py       # Dataset loading and augmentation logic
│   ├── model_utils.py         # Model building architectures (MobileNet, ResNet, etc.)
│   └── validate_dataset.py    # Pre-training dataset integrity validation
└── README.md                  # This file
```

## Dataset Location & Addition

The real PlantVillage dataset is manually placed in:
`backend/ai_engine/disease_detection/datasets/raw/plantvillage/`

**How to add it:**
1. Download the PlantVillage dataset.
2. Extract the dataset so that the class folders (e.g., `Apple___Apple_scab`, `Tomato___healthy`) are located directly inside `backend/ai_engine/disease_detection/datasets/raw/plantvillage/`.
3. Run the validation script to ensure data integrity before training:
   ```bash
   python backend/ai_engine/disease_detection/utils/validate_dataset.py
   ```
   This will output a validation report in the `datasets/processed/` folder.

## How to Train

Run the automated training pipeline. This will train `MobileNetV3`, `EfficientNetB0`, and `ResNet50`, evaluate them, and automatically select the best performing model.

```bash
python backend/ai_engine/disease_detection/training/train_models.py --epochs 10 --batch_size 32
```
Checkpoints will be saved in `models/checkpoints/` and logs in `models/logs/`.

## How to Evaluate

You can evaluate the currently exported production model on an independent test set, and generate a confusion matrix and classification report:

```bash
python backend/ai_engine/disease_detection/evaluation/evaluate_models.py
```

## How to Export the Model

The training script (`train_models.py`) handles the export process automatically. When training finishes, the best architecture is promoted and exported as:
- `disease_production_best.keras`
- `class_names.json`
- `training_metadata.json`

These files are exported directly to:
`backend/ai_engine/models/disease_detection/`

## How the Backend Loads the Model

The Django backend utilizes the `ModelsRegistry` interface (usually located in `backend/ai_engine/models_registry/`) to discover and load active models. 
Because the exported files are saved to `backend/ai_engine/models/disease_detection/`, the backend can seamlessly load `disease_production_best.keras` during startup or lazy-loading for active inference endpoints.

The `inference/predict.py` file also provides a reference `DiseasePredictor` class demonstrating how the model and `class_names.json` are loaded and how image pre-processing and predictions are performed in the backend environment.
