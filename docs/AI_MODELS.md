# AI Models

Dhatree AI employs three primary ML pipelines:

## 1. Crop Recommendation (Random Forest)
- **Dataset**: Built using historical crop data containing N, P, K, temperature, humidity, pH, and rainfall.
- **Training**: StandardScaler + RandomForestClassifier.
- **Location**: \ackend/ai_engine/models/crop_recommendation/best_crop_model.joblib\

## 2. Fertilizer Recommendation (Neural Network)
- **Dataset**: Soil metrics mapped to specific fertilizer types.
- **Training**: TensorFlow Keras Sequential Model.
- **Location**: \ackend/ai_engine/models/fertilizer_recommendation/fertilizer_production_best.joblib\

## 3. Disease Detection (ResNet50 Vision)
- **Dataset**: PlantVillage Dataset (38 classes of crops/diseases).
- **Training**: Transfer learning from ResNet50 (ImageNet).
- **Location**: \ackend/ai_engine/models/disease_detection/disease_production_best.keras\

**Note**: Due to GitHub file size limits, models are omitted from version control. You must run the training scripts located in \scripts/\ to generate them locally, or download them from external releases.

