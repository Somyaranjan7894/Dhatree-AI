from core.repositories import BaseRepository
from modules.disease_detection.models.prediction import DiseasePrediction


class DiseasePredictionRepository(BaseRepository):
    @property
    def model_class(self):
        return DiseasePrediction

    def get_user_predictions(self, user):
        return self.model_class.objects.select_related("user", "farm").filter(user=user)
