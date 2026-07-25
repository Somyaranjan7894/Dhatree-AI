"""
Soil Repository.
"""
from typing import Type
from core.repositories.base import BaseRepository
from modules.soil_analysis.models.soil_sample import SoilSample

class SoilSampleRepository(BaseRepository[SoilSample]):
    @property
    def model_class(self) -> Type[SoilSample]:
        return SoilSample

    def list_active_for_farm(self, farm_id: str):
        return self.model_class.active_objects.filter(farm_id=farm_id)
