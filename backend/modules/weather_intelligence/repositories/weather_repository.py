"""
Weather Snapshot Repository.
"""
from typing import Type
from core.repositories.base import BaseRepository
from modules.weather_intelligence.models.weather_snapshot import WeatherSnapshot

class WeatherSnapshotRepository(BaseRepository[WeatherSnapshot]):
    @property
    def model_class(self) -> Type[WeatherSnapshot]:
        return WeatherSnapshot

    def list_active_for_farm(self, farm_id: str):
        return self.model_class.active_objects.filter(farm_id=farm_id)
