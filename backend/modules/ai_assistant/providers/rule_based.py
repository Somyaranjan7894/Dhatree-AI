import re
from typing import List, Dict
from modules.disease_diagnosis.models.knowledge import Disease
from modules.disease_detection.models.prediction import DiseasePrediction
from modules.fertilizer_recommendation.models.recommendation import FertilizerRecommendation
from .base import BaseProvider

class RuleBasedProvider(BaseProvider):
    def generate_response(self, user, message: str, context_snapshot: Dict, history: List[Dict]) -> str:
        text = message.lower()
        
        if "hello" in text or "hi" in text:
            return "Hello! I am your AI Farming Assistant. You can ask me about your recent scans, fertilizer recommendations, or specific crop diseases."
        
        if "disease" in text or "scan" in text or "sick" in text:
            recent = DiseasePrediction.active_objects.filter(user=user).order_by('-created_at').first()
            if recent:
                name = recent.predicted_class.replace('___', ' - ').replace('_', ' ')
                if "healthy" in name.lower():
                    return f"Your last scan on {recent.created_at.date()} showed that your crop is healthy! No immediate action is required."
                
                diagnosis = Disease.active_objects.filter(name__icontains=recent.predicted_class).first()
                if diagnosis:
                    treatments = diagnosis.treatments.all()
                    treatment_txt = "\n".join([f"- {t.instruction}" for t in treatments])
                    return f"Your last scan detected {name}. \n\nRecommended treatments:\n{treatment_txt}"
                return f"Your last scan detected {name}, but I don't have detailed treatment plans in the knowledge base right now."
            return "You haven't scanned any crops recently. Go to the Disease Detection page to scan a leaf."

        if "fertilizer" in text or "nutrient" in text or "soil" in text:
            recent = FertilizerRecommendation.active_objects.filter(user=user).order_by('-created_at').first()
            if recent:
                return f"Based on your recent soil analysis for {recent.crop_type}, we recommended {recent.recommended_fertilizer}."
            return "I don't see any recent fertilizer recommendations. You can generate one on the Fertilizer Recommendation page by entering your soil NPK values."

        # Fallback to KB search
        if "what is" in text or "how to treat" in text or "about" in text:
            # simple keyword extraction
            words = text.split()
            # Try to find a disease match
            diseases = Disease.active_objects.all()
            for d in diseases:
                if d.name.lower() in text or any(word in d.name.lower() for word in words if len(word) > 4):
                    return f"I found information about {d.name}. Symptoms typically include: {d.symptoms}. You can view more details in the Disease Knowledge Base."
        
        return "I'm not quite sure how to answer that yet. I am currently a rule-based assistant, but I am designed to learn more soon! Try asking about your recent 'scans' or 'fertilizer' recommendations."
