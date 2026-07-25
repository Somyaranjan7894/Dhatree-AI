"""
Crop Repository.
"""

from typing import Type

from core.repositories.base import BaseRepository
from modules.crops.models.crop import Crop


class CropRepository(BaseRepository[Crop]):
    @property
    def model_class(self) -> Type[Crop]:
        return Crop

    def list_active(self, **filters):
        return self.model_class.active_objects.filter(**filters)
