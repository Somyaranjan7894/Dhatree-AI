"""
Weather Service.
"""

from django.db import transaction

from core.services.base import BaseService
from modules.weather_intelligence.models.weather_snapshot import WeatherSnapshot
from modules.weather_intelligence.repositories.weather_repository import (
    WeatherSnapshotRepository,
)


class WeatherService(BaseService):
    def __init__(self):
        super().__init__()
        self.weather_repository = WeatherSnapshotRepository()

    def get_snapshot(self, snapshot_id: str) -> WeatherSnapshot:
        return self.weather_repository.get_by_id_or_raise(snapshot_id)

    def list_snapshots(self, farm_id: str):
        return self.weather_repository.list_active_for_farm(farm_id=farm_id)

    @transaction.atomic
    def create_snapshot(self, farm_id: str, **data) -> WeatherSnapshot:
        data["farm_id"] = farm_id
        self.log_operation("create_weather_snapshot", {"farm_id": farm_id})
        return self.weather_repository.create(**data)

    @transaction.atomic
    def update_snapshot(self, snapshot_id: str, **data) -> WeatherSnapshot:
        snapshot = self.get_snapshot(snapshot_id)
        self.log_operation("update_weather_snapshot", {"snapshot_id": snapshot_id})
        return self.weather_repository.update(snapshot, **data)

    @transaction.atomic
    def delete_snapshot(self, snapshot_id: str) -> None:
        snapshot = self.get_snapshot(snapshot_id)
        self.log_operation("delete_weather_snapshot", {"snapshot_id": snapshot_id})
        snapshot.soft_delete()
