"""
Repositories encapsulating all database queries and transactions for the Farms domain boundary.
Prevents direct ORM calls from Services or Views.
"""

from typing import Any, Optional, Type

from django.db.models.query import QuerySet

from core.repositories.base import BaseRepository
from modules.farms.models.farm import Farm
from modules.farms.models.farm_activity import FarmActivity
from modules.farms.models.farm_crop import FarmCrop
from modules.farms.models.farm_image import FarmImage


class FarmRepository(BaseRepository[Farm]):
    """Data access repository for Farm entities."""

    @property
    def model_class(self) -> Type[Farm]:
        return Farm

    def get_by_id(self, entity_id: Any) -> Optional[Farm]:
        """Retrieve a farm by ID using `active_objects` to exclude soft deleted farms."""
        try:
            return self.model_class.active_objects.get(pk=entity_id)
        except self.model_class.DoesNotExist:
            return None

    def list_by_owner(self, owner_id: Any, **filters: Any) -> QuerySet[Farm]:
        """Retrieve all active farms belonging to a specific owner profile."""
        return self.model_class.active_objects.select_related("owner").filter(
            owner_id=owner_id, **filters
        )

    def list_active(self, **filters: Any) -> QuerySet[Farm]:
        """Retrieve all non-deleted farms."""
        return self.model_class.active_objects.select_related("owner").filter(**filters)

    def check_duplicate_farm_name(
        self, owner_id: Any, farm_name: str, exclude_farm_id: Optional[Any] = None
    ) -> bool:
        """Check if an active farm with the same name already exists for this owner."""
        if not farm_name or not owner_id:
            return False
        qs = self.model_class.active_objects.filter(
            owner_id=owner_id, farm_name__iexact=farm_name.strip()
        )
        if exclude_farm_id:
            qs = qs.exclude(pk=exclude_farm_id)
        return qs.exists()

    def soft_delete(self, farm: Farm) -> None:
        """Execute soft deletion on a farm instance."""
        farm.soft_delete()

    def archive(self, farm: Farm) -> None:
        """Archive a farm instance."""
        farm.archive()


class FarmCropRepository(BaseRepository[FarmCrop]):
    """Data access repository for FarmCrop entities."""

    @property
    def model_class(self) -> Type[FarmCrop]:
        return FarmCrop

    def get_by_id(self, entity_id: Any) -> Optional[FarmCrop]:
        try:
            return self.model_class.active_objects.get(pk=entity_id)
        except self.model_class.DoesNotExist:
            return None

    def list_by_farm(self, farm_id: Any, **filters: Any) -> QuerySet[FarmCrop]:
        """Retrieve active crop cycles cultivated on a specific farm."""
        return self.model_class.active_objects.filter(farm_id=farm_id, **filters)

    def soft_delete(self, farm_crop: FarmCrop) -> None:
        farm_crop.soft_delete()


class FarmImageRepository(BaseRepository[FarmImage]):
    """Data access repository for FarmImage entities."""

    @property
    def model_class(self) -> Type[FarmImage]:
        return FarmImage

    def get_by_id(self, entity_id: Any) -> Optional[FarmImage]:
        try:
            return self.model_class.active_objects.get(pk=entity_id)
        except self.model_class.DoesNotExist:
            return None

    def list_by_farm(self, farm_id: Any, **filters: Any) -> QuerySet[FarmImage]:
        """Retrieve active images for a specific farm."""
        return self.model_class.active_objects.filter(farm_id=farm_id, **filters)

    def soft_delete(self, farm_image: FarmImage) -> None:
        farm_image.soft_delete()


class FarmActivityRepository(BaseRepository[FarmActivity]):
    """Data access repository for FarmActivity entities."""

    @property
    def model_class(self) -> Type[FarmActivity]:
        return FarmActivity

    def get_by_id(self, entity_id: Any) -> Optional[FarmActivity]:
        try:
            return self.model_class.active_objects.get(pk=entity_id)
        except self.model_class.DoesNotExist:
            return None

    def list_by_farm(self, farm_id: Any, **filters: Any) -> QuerySet[FarmActivity]:
        """Retrieve chronological history log entries for a specific farm."""
        return self.model_class.active_objects.filter(farm_id=farm_id, **filters)

    def soft_delete(self, farm_activity: FarmActivity) -> None:
        farm_activity.soft_delete()
