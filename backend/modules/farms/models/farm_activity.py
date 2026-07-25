"""
FarmActivity model definition for Dhatree AI Agriculture Platform.
Stores chronological agricultural activity history logs for farms and crop cycles.
"""
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ActiveFarmActivityManager(models.Manager):
    """Manager returning only non-deleted (`is_deleted=False`) active FarmActivity instances."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class FarmActivity(models.Model):
    """
    Chronological record of field activities (sowing, irrigation, weeding, harvest) performed on a farm.
    """

    class ActivityType(models.TextChoices):
        SOWING = "sowing", _("Sowing / Planting")
        IRRIGATION = "irrigation", _("Irrigation / Watering")
        FERTILIZER_APPLICATION = "fertilizer_application", _("Fertilizer / Manure Application")
        PESTICIDE_APPLICATION = "pesticide_application", _("Pesticide / Herbicide Application")
        WEEDING = "weeding", _("Weeding / Cleaning")
        SOIL_TESTING = "soil_testing", _("Soil Sampling / Testing")
        HARVESTING = "harvesting", _("Harvesting")
        OBSERVATION = "observation", _("Field Observation / Scouing")
        GENERAL_MAINTENANCE = "general_maintenance", _("General Maintenance / Repair")
        OTHER = "other", _("Other Activity")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Unique UUID v4 primary key for this activity log entry."),
    )
    farm = models.ForeignKey(
        "farms.Farm",
        on_delete=models.CASCADE,
        related_name="activities",
        db_index=True,
    )
    farm_crop = models.ForeignKey(
        "farms.FarmCrop",
        on_delete=models.SET_NULL,
        related_name="activities",
        blank=True,
        null=True,
    )
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="performed_activities",
        blank=True,
        null=True,
    )
    activity_type = models.CharField(
        _("activity type"),
        max_length=40,
        choices=ActivityType.choices,
        default=ActivityType.OBSERVATION,
        db_index=True,
    )
    activity_date = models.DateField(
        _("activity date"),
        default=timezone.now,
    )
    title = models.CharField(
        _("activity title"),
        max_length=255,
    )
    description = models.TextField(
        _("activity details"),
        blank=True,
    )
    cost_incurred = models.DecimalField(
        _("cost incurred"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
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
    active_objects = ActiveFarmActivityManager()

    class Meta:
        verbose_name = _("farm activity")
        verbose_name_plural = _("farm activities")
        ordering = ["-activity_date", "-created_at"]
        indexes = [
            models.Index(fields=["farm", "activity_type", "is_deleted"]),
            models.Index(fields=["activity_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.title} on {self.farm.farm_name} ({self.activity_date})"

    def soft_delete(self) -> None:
        """Marks the activity log as deleted without removing historical records."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at", "updated_at"])
