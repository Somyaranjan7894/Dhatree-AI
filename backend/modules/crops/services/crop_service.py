"""
Crop Service.
"""

from typing import Any

from django.db import transaction

from core.services.base import BaseService
from modules.crops.models.crop import Crop
from modules.crops.repositories.crop_repository import CropRepository


class CropService(BaseService):
    def __init__(self):
        super().__init__()
        self.crop_repository = CropRepository()

    def get_crop(self, crop_id: str) -> Crop:
        return self.crop_repository.get_by_id_or_raise(crop_id)

    def list_crops(self) -> Any:
        return self.crop_repository.list_active()

    @transaction.atomic
    def create_crop(self, **data) -> Crop:
        self.log_operation("create_crop", {"crop_name": data.get("crop_name")})
        return self.crop_repository.create(**data)

    @transaction.atomic
    def update_crop(self, crop_id: str, **data) -> Crop:
        crop = self.get_crop(crop_id)
        self.log_operation("update_crop", {"crop_id": crop_id})
        return self.crop_repository.update(crop, **data)

    @transaction.atomic
    def delete_crop(self, crop_id: str) -> None:
        crop = self.get_crop(crop_id)
        self.log_operation("delete_crop", {"crop_id": crop_id})
        crop.soft_delete()
