"""
FarmCrop model definition for Dhatree AI Agriculture Platform.
Represents a specific crop cycle (sowing to harvest) on a Farm parcel.
"""
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ActiveFarmCropManager(models.Manager):
    """Manager returning only non-deleted (`is_deleted=False`) active FarmCrop instances."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class FarmCrop(models.Model):
    """
    Tracks a specific crop cycle cultivated on a Farm.
    Links the Farm entity to the global Crop Master directory (`modules.crops.Crop`).
    """

    class CropStatus(models.TextChoices):
        SOWN = "sown", _("Sown / Planted")
        VEGETATIVE = "vegetative", _("Vegetative Stage")
        FLOWERING = "flowering", _("Flowering Stage")
        FRUITING = "fruiting", _("Fruiting / Podding Stage")
        HARVESTED = "harvested", _("Harvested")
        FAILED = "failed", _("Failed / Damaged")
        ARCHIVED = "archived", _("Archived")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Unique UUID v4 primary key for this farm crop cycle."),
    )
    farm = models.ForeignKey(
        "farms.Farm",
        on_delete=models.CASCADE,
        related_name="farm_crops",
        db_index=True,
        help_text=_("Farm parcel where this crop is being cultivated."),
    )
    crop = models.ForeignKey(
        "crops.Crop",
        on_delete=models.PROTECT,
        related_name="farm_cultivations",
        db_index=True,
        help_text=_("Global Crop Master reference."),
    )
    variety = models.CharField(
        _("crop variety / seed strain"),
        max_length=100,
        blank=True,
    )
    sowing_date = models.DateField(
        _("sowing / planting date"),
    )
    expected_harvest_date = models.DateField(
        _("expected harvest date"),
        blank=True,
        null=True,
    )
    actual_harvest_date = models.DateField(
        _("actual harvest date"),
        blank=True,
        null=True,
    )
    area_allocated = models.DecimalField(
        _("area allocated"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Land area allocated to this specific crop cycle (in Farm unit)."),
    )
    status = models.CharField(
        _("crop cycle status"),
        max_length=30,
        choices=CropStatus.choices,
        default=CropStatus.SOWN,
        db_index=True,
    )
    estimated_yield_kg = models.DecimalField(
        _("estimated yield (kg)"),
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    actual_yield_kg = models.DecimalField(
        _("actual yield (kg)"),
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    notes = models.TextField(
        _("cultivation notes"),
        blank=True,
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
    )
    is_deleted = models.BooleanField(
        _("soft deleted"),
        default=False,
        db_index=True,
    )
    deleted_at = models.DateTimeField(
        _("deleted at"),
        blank=True,
        null=True,
    )

    objects = models.Manager()
    active_objects = ActiveFarmCropManager()

    class Meta:
        verbose_name = _("farm crop")
        verbose_name_plural = _("farm crops")
        ordering = ["-sowing_date", "-created_at"]
        indexes = [
            models.Index(fields=["farm", "status", "is_deleted"]),
            models.Index(fields=["crop", "sowing_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.crop} on {self.farm.farm_name} ({self.sowing_date})"

    def soft_delete(self) -> None:
        """Marks the farm crop cycle as deleted without scrubbing database records."""
        self.is_deleted = True
        self.status = self.CropStatus.ARCHIVED
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "status", "deleted_at", "updated_at"])
