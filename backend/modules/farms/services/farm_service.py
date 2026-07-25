"""
Services orchestrating farm lifecycle, crop cycles, images, and history activities.
Decouples views from Repositories and enforces all business invariants.
"""

from decimal import Decimal
from typing import Any, Dict, Optional

from django.db.models.query import QuerySet

from core.exceptions import ResourceNotFoundError, ValidationError
from core.services.base import BaseService
from modules.farms.models.farm import Farm
from modules.farms.models.farm_activity import FarmActivity
from modules.farms.models.farm_crop import FarmCrop
from modules.farms.models.farm_image import FarmImage
from modules.farms.repositories.farm_repository import (
    FarmActivityRepository,
    FarmCropRepository,
    FarmImageRepository,
    FarmRepository,
)


class FarmService(BaseService):
    """Business service for Farm profile management and domain constraints."""

    def __init__(self, farm_repository: Optional[FarmRepository] = None) -> None:
        super().__init__()
        self.farm_repo = farm_repository or FarmRepository()

    def _validate_coordinates(
        self, latitude: Optional[Any], longitude: Optional[Any]
    ) -> None:
        if latitude is not None and latitude != "":
            try:
                lat_val = Decimal(str(latitude))
                if lat_val < Decimal("-90.0") or lat_val > Decimal("90.0"):
                    raise ValidationError(
                        "Latitude must be between -90.0 and 90.0 degrees."
                    )
            except (ValueError, TypeError):
                raise ValidationError("Invalid latitude coordinate.")

        if longitude is not None and longitude != "":
            try:
                lon_val = Decimal(str(longitude))
                if lon_val < Decimal("-180.0") or lon_val > Decimal("180.0"):
                    raise ValidationError(
                        "Longitude must be between -180.0 and 180.0 degrees."
                    )
            except (ValueError, TypeError):
                raise ValidationError("Invalid longitude coordinate.")

    def _validate_area(self, area: Any) -> None:
        try:
            area_val = Decimal(str(area))
            if area_val <= Decimal("0"):
                raise ValidationError("Total farm area must be greater than 0.")
        except (ValueError, TypeError):
            raise ValidationError("Invalid decimal number for farm area.")

    def create_farm(self, owner: Any, **farm_data: Any) -> Farm:
        """Create a new farm after verifying area, coordinates, and uniqueness invariants."""
        self.log_operation(
            "create_farm",
            {"owner_id": str(owner.id), "farm_name": farm_data.get("farm_name")},
        )

        area = farm_data.get("area")
        if area is not None:
            self._validate_area(area)
        else:
            raise ValidationError("Total area is required.")

        self._validate_coordinates(
            farm_data.get("latitude"), farm_data.get("longitude")
        )

        farm_name = farm_data.get("farm_name", "").strip()
        if not farm_name:
            raise ValidationError("Farm name is required.")

        if self.farm_repo.check_duplicate_farm_name(owner.id, farm_name):
            raise ValidationError(
                f"You already have an active farm named '{farm_name}'."
            )

        farm_data["owner"] = owner
        farm_data["farm_name"] = farm_name
        return self.farm_repo.create(**farm_data)

    def get_farm(self, farm_id: Any) -> Farm:
        """Retrieve an active farm profile by ID."""
        self.log_operation("get_farm", {"farm_id": str(farm_id)})
        return self.farm_repo.get_by_id_or_raise(farm_id)

    def list_farms(
        self, owner_id: Optional[Any] = None, **filters: Any
    ) -> QuerySet[Farm]:
        """List active farms filtered by owner or administrative query parameters."""
        self.log_operation(
            "list_farms", {"owner_id": str(owner_id) if owner_id else "all", **filters}
        )
        if owner_id:
            return self.farm_repo.list_by_owner(owner_id, **filters)
        return self.farm_repo.list_active(**filters)

    def update_farm(self, farm_id: Any, **update_data: Any) -> Farm:
        """Update farm attributes while preserving domain validation rules."""
        self.log_operation(
            "update_farm", {"farm_id": str(farm_id), "fields": list(update_data.keys())}
        )
        farm = self.farm_repo.get_by_id_or_raise(farm_id)

        if "area" in update_data and update_data["area"] is not None:
            self._validate_area(update_data["area"])

        if "latitude" in update_data or "longitude" in update_data:
            lat = update_data.get("latitude", farm.latitude)
            lon = update_data.get("longitude", farm.longitude)
            self._validate_coordinates(lat, lon)

        if "farm_name" in update_data and update_data["farm_name"] is not None:
            farm_name = update_data["farm_name"].strip()
            if not farm_name:
                raise ValidationError("Farm name cannot be empty.")
            if farm_name.lower() != farm.farm_name.lower():
                if self.farm_repo.check_duplicate_farm_name(
                    farm.owner.id, farm_name, exclude_farm_id=farm.id
                ):
                    raise ValidationError(
                        f"You already have an active farm named '{farm_name}'."
                    )
            update_data["farm_name"] = farm_name

        # Prevent owner re-assignment via generic update
        update_data.pop("owner", None)
        update_data.pop("is_deleted", None)

        return self.farm_repo.update(farm, **update_data)

    def soft_delete_farm(self, farm_id: Any) -> None:
        """Soft delete a farm account and transition its status."""
        self.log_operation("soft_delete_farm", {"farm_id": str(farm_id)})
        farm = self.farm_repo.get_by_id_or_raise(farm_id)
        self.farm_repo.soft_delete(farm)

    def archive_farm(self, farm_id: Any) -> Farm:
        """Transitions a farm to archived status."""
        self.log_operation("archive_farm", {"farm_id": str(farm_id)})
        farm = self.farm_repo.get_by_id_or_raise(farm_id)
        self.farm_repo.archive(farm)
        return farm


class FarmCropService(BaseService):
    """Business service managing crop cultivation cycles across farm parcels."""

    def __init__(
        self, farm_crop_repository: Optional[FarmCropRepository] = None
    ) -> None:
        super().__init__()
        self.farm_crop_repo = farm_crop_repository or FarmCropRepository()
        self.farm_repo = FarmRepository()

    def create_farm_crop(self, farm_id: Any, crop_id: Any, **data: Any) -> FarmCrop:
        self.log_operation(
            "create_farm_crop", {"farm_id": str(farm_id), "crop_id": str(crop_id)}
        )
        farm = self.farm_repo.get_by_id_or_raise(farm_id)

        area_allocated = data.get("area_allocated")
        if area_allocated is not None:
            try:
                area_val = Decimal(str(area_allocated))
                if area_val <= Decimal("0"):
                    raise ValidationError("Allocated area must be greater than 0.")
                if area_val > farm.area:
                    raise ValidationError(
                        f"Allocated area ({area_val}) cannot exceed total farm area ({farm.area})."
                    )
            except (ValueError, TypeError):
                raise ValidationError("Invalid decimal number for allocated area.")
        else:
            raise ValidationError("Allocated area is required for crop cycle.")

        sowing_date = data.get("sowing_date")
        expected_harvest = data.get("expected_harvest_date")
        if sowing_date and expected_harvest and expected_harvest <= sowing_date:
            raise ValidationError("Expected harvest date must be after sowing date.")

        data["farm"] = farm
        data["crop_id"] = crop_id
        return self.farm_crop_repo.create(**data)

    def get_farm_crop(self, farm_crop_id: Any) -> FarmCrop:
        return self.farm_crop_repo.get_by_id_or_raise(farm_crop_id)

    def list_farm_crops(self, farm_id: Any, **filters: Any) -> QuerySet[FarmCrop]:
        self.farm_repo.get_by_id_or_raise(farm_id)
        return self.farm_crop_repo.list_by_farm(farm_id, **filters)

    def update_farm_crop(self, farm_crop_id: Any, **data: Any) -> FarmCrop:
        farm_crop = self.farm_crop_repo.get_by_id_or_raise(farm_crop_id)

        if "area_allocated" in data and data["area_allocated"] is not None:
            area_val = Decimal(str(data["area_allocated"]))
            if area_val <= Decimal("0"):
                raise ValidationError("Allocated area must be greater than 0.")
            if area_val > farm_crop.farm.area:
                raise ValidationError(
                    f"Allocated area ({area_val}) cannot exceed total farm area ({farm_crop.farm.area})."
                )

        sowing_date = data.get("sowing_date", farm_crop.sowing_date)
        expected_harvest = data.get(
            "expected_harvest_date", farm_crop.expected_harvest_date
        )
        if sowing_date and expected_harvest and expected_harvest <= sowing_date:
            raise ValidationError("Expected harvest date must be after sowing date.")

        data.pop("farm", None)
        data.pop("is_deleted", None)
        return self.farm_crop_repo.update(farm_crop, **data)

    def soft_delete_farm_crop(self, farm_crop_id: Any) -> None:
        farm_crop = self.farm_crop_repo.get_by_id_or_raise(farm_crop_id)
        self.farm_crop_repo.soft_delete(farm_crop)


class FarmImageService(BaseService):
    """Business service managing visual observations across farms."""

    def __init__(
        self, farm_image_repository: Optional[FarmImageRepository] = None
    ) -> None:
        super().__init__()
        self.farm_image_repo = farm_image_repository or FarmImageRepository()
        self.farm_repo = FarmRepository()

    def upload_image(self, farm_id: Any, **data: Any) -> FarmImage:
        self.log_operation("upload_image", {"farm_id": str(farm_id)})
        farm = self.farm_repo.get_by_id_or_raise(farm_id)
        if not data.get("image"):
            raise ValidationError("An image file is required.")
        data["farm"] = farm
        return self.farm_image_repo.create(**data)

    def get_image(self, image_id: Any) -> FarmImage:
        return self.farm_image_repo.get_by_id_or_raise(image_id)

    def list_images(self, farm_id: Any, **filters: Any) -> QuerySet[FarmImage]:
        self.farm_repo.get_by_id_or_raise(farm_id)
        return self.farm_image_repo.list_by_farm(farm_id, **filters)

    def delete_image(self, image_id: Any) -> None:
        image = self.farm_image_repo.get_by_id_or_raise(image_id)
        self.farm_image_repo.soft_delete(image)


class FarmActivityService(BaseService):
    """Business service managing chronological activity history logs."""

    def __init__(
        self, farm_activity_repository: Optional[FarmActivityRepository] = None
    ) -> None:
        super().__init__()
        self.farm_activity_repo = farm_activity_repository or FarmActivityRepository()
        self.farm_repo = FarmRepository()

    def log_activity(
        self, farm_id: Any, performed_by: Optional[Any] = None, **data: Any
    ) -> FarmActivity:
        self.log_operation(
            "log_activity",
            {"farm_id": str(farm_id), "activity_type": data.get("activity_type")},
        )
        farm = self.farm_repo.get_by_id_or_raise(farm_id)

        if not data.get("title") or not str(data.get("title")).strip():
            raise ValidationError("Activity title is required.")

        cost = data.get("cost_incurred")
        if cost is not None:
            try:
                if Decimal(str(cost)) < Decimal("0"):
                    raise ValidationError("Cost incurred cannot be negative.")
            except (ValueError, TypeError):
                raise ValidationError("Invalid decimal format for cost incurred.")

        data["farm"] = farm
        if performed_by:
            data["performed_by"] = performed_by
        return self.farm_activity_repo.create(**data)

    def get_activity(self, activity_id: Any) -> FarmActivity:
        return self.farm_activity_repo.get_by_id_or_raise(activity_id)

    def list_activities(self, farm_id: Any, **filters: Any) -> QuerySet[FarmActivity]:
        self.farm_repo.get_by_id_or_raise(farm_id)
        return self.farm_activity_repo.list_by_farm(farm_id, **filters)

    def update_activity(self, activity_id: Any, **data: Any) -> FarmActivity:
        activity = self.farm_activity_repo.get_by_id_or_raise(activity_id)
        if "cost_incurred" in data and data["cost_incurred"] is not None:
            if Decimal(str(data["cost_incurred"])) < Decimal("0"):
                raise ValidationError("Cost incurred cannot be negative.")
        data.pop("farm", None)
        data.pop("performed_by", None)
        return self.farm_activity_repo.update(activity, **data)

    def delete_activity(self, activity_id: Any) -> None:
        activity = self.farm_activity_repo.get_by_id_or_raise(activity_id)
        self.farm_activity_repo.soft_delete(activity)
