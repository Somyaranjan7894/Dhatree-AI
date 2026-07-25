"""
Soil Service.
"""
from django.db import transaction
from core.services.base import BaseService
from modules.soil_analysis.models.soil_sample import SoilSample
from modules.soil_analysis.repositories.soil_repository import SoilSampleRepository

class SoilService(BaseService):
    def __init__(self):
        super().__init__()
        self.soil_repository = SoilSampleRepository()

    def get_sample(self, sample_id: str) -> SoilSample:
        return self.soil_repository.get_by_id_or_raise(sample_id)

    def list_samples(self, farm_id: str):
        return self.soil_repository.list_active_for_farm(farm_id=farm_id)

    @transaction.atomic
    def create_sample(self, farm_id: str, **data) -> SoilSample:
        data["farm_id"] = farm_id
        self.log_operation("create_soil_sample", {"farm_id": farm_id})
        return self.soil_repository.create(**data)

    @transaction.atomic
    def update_sample(self, sample_id: str, **data) -> SoilSample:
        sample = self.get_sample(sample_id)
        self.log_operation("update_soil_sample", {"sample_id": sample_id})
        return self.soil_repository.update(sample, **data)

    @transaction.atomic
    def delete_sample(self, sample_id: str) -> None:
        sample = self.get_sample(sample_id)
        self.log_operation("delete_soil_sample", {"sample_id": sample_id})
        sample.soft_delete()
