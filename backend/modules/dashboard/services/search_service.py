from typing import Dict, List

from django.db.models import Q

from modules.crop_recommendation.models.recommendation import CropRecommendation
from modules.disease_detection.models.prediction import DiseasePrediction
from modules.disease_diagnosis.models.knowledge import Disease
from modules.farms.models.farm import Farm
from modules.fertilizer_recommendation.models.recommendation import (
    FertilizerRecommendation,
)


class GlobalSearchService:
    def search(self, user, query: str) -> Dict[str, List[Dict]]:
        """
        Categorized and fuzzy search across the platform.
        """
        results = {
            "farms": [],
            "diseases": [],
            "predictions": [],
            "recommendations": [],
        }

        if not query or len(query) < 2:
            return results

        # 1. Search Farms
        farms = Farm.active_objects.filter(
            Q(owner=user) & (Q(name__icontains=query) | Q(location__icontains=query))
        )[:5]
        for f in farms:
            results["farms"].append(
                {
                    "id": str(f.id),
                    "title": f.name,
                    "description": f.location,
                    "type": "farm",
                }
            )

        # 2. Search Disease Knowledge Base
        diseases = Disease.objects.filter(
            Q(name__icontains=query) | Q(symptoms__icontains=query)
        )[:5]
        for d in diseases:
            results["diseases"].append(
                {
                    "id": str(d.id),
                    "title": d.name,
                    "description": d.symptoms[:100] + "...",
                    "type": "knowledge",
                }
            )

        # 3. Search Prediction History
        preds = DiseasePrediction.active_objects.filter(
            Q(user=user) & Q(predicted_class__icontains=query)
        )[:5]
        for p in preds:
            results["predictions"].append(
                {
                    "id": str(p.id),
                    "title": p.predicted_class.replace("___", " - ").replace("_", " "),
                    "description": f"Confidence: {(p.confidence_score*100):.1f}%",
                    "type": "prediction",
                }
            )

        # 4. Search Recommendations
        crop_recs = CropRecommendation.active_objects.filter(
            Q(user=user) & Q(recommended_crop__icontains=query)
        )[:3]
        for c in crop_recs:
            results["recommendations"].append(
                {
                    "id": str(c.id),
                    "title": c.recommended_crop,
                    "description": "Crop Recommendation",
                    "type": "crop_rec",
                }
            )

        fert_recs = FertilizerRecommendation.active_objects.filter(
            Q(user=user)
            & (
                Q(crop_type__icontains=query)
                | Q(recommended_fertilizer__icontains=query)
            )
        )[:3]
        for f in fert_recs:
            results["recommendations"].append(
                {
                    "id": str(f.id),
                    "title": f.recommended_fertilizer,
                    "description": f"Fertilizer for {f.crop_type}",
                    "type": "fert_rec",
                }
            )

        return results
