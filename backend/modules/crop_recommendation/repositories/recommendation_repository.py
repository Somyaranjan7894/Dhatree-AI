from core.repositories.base import BaseRepository
from modules.crop_recommendation.models.recommendation import CropRecommendation

class CropRecommendationRepository(BaseRepository):
    @property
    def model_class(self):
        return CropRecommendation

    def get_user_recommendations(self, user):
        return self.model_class.objects.select_related('user', 'farm').filter(user=user)
