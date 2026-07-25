# Dhatree AI

**AI-powered Agriculture Intelligence Platform.**

Dhatree AI is a comprehensive enterprise-grade platform designed to assist farmers and agronomists with precision agriculture. It leverages Artificial Intelligence to provide crop recommendations, fertilizer suggestions, plant disease detection, and real-time agricultural chat assistance.

## Problem Statement
Modern farming requires data-driven decision making. Farmers face challenges in identifying the right crops for their specific soil metrics, determining optimal fertilizer dosages, and accurately diagnosing plant diseases before they spread. 

## Key Features
- **Crop Recommendation**: Recommends the most suitable crop based on N, P, K levels, pH, temperature, humidity, and rainfall.
- **Fertilizer Recommendation**: Suggests optimal fertilizer type and dosage tailored to soil health and crop type.
- **Disease Detection**: Uses Computer Vision (ResNet50) to classify plant diseases from leaf images.
- **Gemini AI Assistant**: A conversational AI specifically tuned for agricultural advice.
- **Farm & Soil Management**: Manage multiple farms and track historical soil records.
- **Unified Recommendations Dashboard**: View and analyze combined intelligence reports.

## System Architecture
Dhatree AI uses a **Modular Monolith** architecture to keep deployment simple while maintaining strict domain boundaries.

- **Frontend**: React 18, TypeScript, Vite, TailwindCSS.
- **Backend**: Django, Django REST Framework, SimpleJWT.
- **AI Engine**: TensorFlow/Keras, Scikit-Learn, Google GenAI (Gemini).
- **Database**: PostgreSQL for relational data, Redis for caching and Celery message brokering.

## AI & ML Models
- **Crop Recommendation**: Trained on soil metrics using a Random Forest Classifier.
- **Fertilizer Recommendation**: Multi-layer Perceptron (Neural Network) predicting optimal NPK adjustments and fertilizer types.
- **Disease Detection**: A ResNet50 Convolutional Neural Network trained on the PlantVillage dataset (38 classes).

> **Important Note regarding Disease Detection Performance:**
> The model achieves high accuracy (>95%) on the PlantVillage benchmark dataset. However, PlantVillage consists of single leaves against controlled backgrounds. *Benchmark performance does not necessarily represent real-world field-image performance where lighting, background clutter, and multiple leaves are present.* 

## Project Structure
```text
dhatree_AI/
├── backend/          # Django Backend (Modular Monolith)
│   ├── ai_engine/    # ML Pipelines & Registry
│   ├── core/         # Shared Utilities
│   └── modules/      # Domain-Driven Modules (farms, crops, ai_assistant)
├── frontend/         # React SPA
├── docker/           # Docker Compose Configurations
├── docs/             # Technical Documentation
└── scripts/          # Utility Scripts
```

## Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL
- Redis (Optional, required for Celery workers)

### 1. Environment Configuration
Copy `.env.example` to `.env` and fill in your details:
```bash
cp .env.example .env
```
*Make sure to provide a valid `GEMINI_API_KEY` to use the AI Assistant feature.*

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements/development.txt
python manage.py migrate
python manage.py runserver
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Docker Usage
To run the complete stack (Postgres, Redis, Backend, Celery, Frontend) using Docker:
```bash
cd docker
docker-compose up --build
```

## AI Model Setup
The repository does *not* contain the heavy `.keras` or `.joblib` model files due to GitHub size limits.
Please refer to the `docs/AI_MODELS.md` documentation for instructions on how to train or download the production artifacts.

## Testing
- **Backend**: Run `pytest` inside the `backend` directory.
- **Frontend**: Run `npm test` inside the `frontend` directory.

## Known Limitations
- Disease detection models struggle with multi-leaf field images due to PlantVillage dataset biases.
- Weather integration is currently a mocked service placeholder for future 3rd-party API integration.

## Future Roadmap
- Integration with live weather APIs (OpenWeatherMap).
- YOLOv8 implementation for multi-leaf field disease detection.
- Mobile App (React Native).

## Contributing
Please see `CONTRIBUTING.md` for guidelines.

## License
This project is licensed under the MIT License - see the `LICENSE` file for details.
