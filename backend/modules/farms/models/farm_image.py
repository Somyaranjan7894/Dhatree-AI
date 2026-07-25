"""
FarmImage model definition for Dhatree AI Agriculture Platform.
Stores visual imagery captured across farms or specific crop cycles.
"""
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ActiveFarmImageManager(models.Manager):
    """Manager returning only non-deleted (`is_deleted=False`) active FarmImage instances."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class FarmImage(models.Model):
    """
    Visual image observation associated with a Farm or a specific FarmCrop cycle.
    """

    class ImageType(models.TextChoices):
        GENERAL = "general", _("General Farm View")
        CROP_PROGRESS = "crop_progress", _("Crop Growth Progress")
        SOIL_CONDITION = "soil_condition", _("Soil Condition")
        PEST_DISEASE_OBSERVATION = "pest_disease_observation", _("Pest / Disease Observation")
        HARVEST = "harvest", _("Harvesting Stage")
        OTHER = "other", _("Other / Miscellaneous")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Unique UUID v4 primary key for this farm image."),
    )
    farm = models.ForeignKey(
        "farms.Farm",
        on_delete=models.CASCADE,
        related_name="images",
        db_index=True,
    )
    farm_crop = models.ForeignKey(
        "farms.FarmCrop",
        on_delete=models.SET_NULL,
        related_name="images",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        _("image file"),
        upload_to="farm_images/%Y/%m/",
    )
    image_type = models.CharField(
        _("image category"),
        max_length=40,
        choices=ImageType.choices,
        default=ImageType.GENERAL,
        db_index=True,
    )
    caption = models.CharField(
        _("image caption"),
        max_length=255,
        blank=True,
    )
    taken_at = models.DateTimeField(
        _("captured timestamp"),
        default=timezone.now,
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
    active_objects = ActiveFarmImageManager()

    class Meta:
        verbose_name = _("farm image")
        verbose_name_plural = _("farm images")
        ordering = ["-taken_at", "-created_at"]
        indexes = [
            models.Index(fields=["farm", "image_type", "is_deleted"]),
        ]

    def __str__(self) -> str:
        return f"{self.get_image_type_display()} - {self.farm.farm_name}"

    def soft_delete(self) -> None:
        """Marks the image record as deleted without removing underlying physical files immediately."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])
