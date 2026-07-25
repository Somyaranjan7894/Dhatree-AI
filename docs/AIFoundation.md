# AI Foundation & Training Infrastructure

The **Phase 5 AI Foundation** establishes a strictly decoupled workspace dedicated to machine learning dataset processing, model training, evaluation, and iteration. This architecture ensures that AI/Data Science tasks do not leak into the web server (`backend/`) logic, adhering to the project's separation of concerns.

## Directory Structure

```text
ai/
├── common/                # Shared utilities across AI domains
├── config/                # Environment and hyperparameter configuration
├── datasets/              
│   ├── raw/               # Unmodified source data
│   ├── processed/         # Cleaned/Normalized datasets ready for training
│   ├── sample/            # Small subset used for fast testing/dev
│   └── metadata/          # JSON reports for dataset validation
├── preprocessing/         # Image augmentation and transformation classes
├── training/              # Reusable epoch-driven PyTorch training loops
├── inference/             # Model loading and forward pass pipeline
├── evaluation/            # Scikit-learn integration for classification metrics
├── models/                # Saved checkpoints (.pth) and metadata (.json)
├── utils/                 # Standardized logging mechanisms
├── disease_detection/     # Domain-specific training logic (Phase 6+)
├── crop_recommendation/   # Domain-specific training logic (Phase 6+)
├── notebooks/             # Jupyter notebooks for data exploration
└── tests/                 # Unit tests for the AI utilities
```

## Key Components

### 1. Configuration (`ai.config.settings`)
Centralizes all magic numbers and paths. Modifying batch sizes, epochs, learning rates, or image dimensions should be done strictly through the `AIConfig` class, rather than hardcoding values in scripts.

### 2. Dataset Utilities (`ai.datasets.dataset_utils`)
`DatasetManager` provides automated validation against corrupted image files, ensures correct subfolder categorization for `torchvision.datasets.ImageFolder`, and generates printable metadata summaries.

### 3. Preprocessing (`ai.preprocessing.image_processor`)
`BaseImageProcessor` manages PyTorch `transforms` pipelines, converting PIL Images, Numpy Arrays, and raw file paths into normalized Tensors safely (enforcing RGB).

### 4. Training Engine (`ai.training.trainer`)
The `BaseTrainer` abstracts away the boilerplate of PyTorch training loops.
- Automatically handles CPU vs GPU (`cuda`) distribution.
- Tracks metrics across epochs.
- Implements Early Stopping automatically based on Validation Loss.
- Injects Learning Rate Schedulers dynamically.

### 5. Model Management (`ai.models.model_manager`)
The `ModelManager` seamlessly persists state dictionaries, optimizing the workflow so you can load the specific `best.pth` artifact independently into the Django backend API later.

### 6. Inference & Evaluation
- `BaseInferencer`: Standardizes raw predictions into robust confidence percentages.
- `ModelEvaluator`: Connects ground-truth outputs with PyTorch predictions into standard Sci-Kit Learn confusion matrices and classification reports.

## Running Tests

To verify the AI utilities locally (mocking out the GPU dependencies if `torch` is not installed):
```powershell
$env:PYTHONPATH="."
backend\venv\Scripts\pytest ai/tests/
```
