"""
Farm model definition for Dhatree AI Agriculture Platform.
Represents a geographical farming unit owned/managed by a User (Farmer).
"""
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ActiveFarmManager(models.Manager):
    """Manager returning only non-deleted (`is_deleted=False`) active Farm instances."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Farm(models.Model):
    """
    Geographical and operational agricultural unit managed by a platform user.
    Uses UUID v4 primary key, precise area/coordinate tracking, and soft deletion.
    """

    class AreaUnit(models.TextChoices):
        ACRES = "acres", _("Acres")
        HECTARES = "hectares", _("Hectares")
        SQ_METERS = "sq_meters", _("Square Meters")

    class WaterSource(models.TextChoices):
        CANAL = "canal", _("Canal Irrigation")
        TUBE_WELL = "tube_well", _("Tube Well / Borewell")
        OPEN_WELL = "open_well", _("Open Well")
        RAINFED = "rainfed", _("Rainfed / Monsoon")
        DRIP_IRRIGATION = "drip_irrigation", _("Drip Irrigation System")
        SPRINKLER = "sprinkler", _("Sprinkler Irrigation System")
        OTHER = "other", _("Other / Mixed")

    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        INACTIVE = "inactive", _("Inactive / Fallow")
        ARCHIVED = "archived", _("Archived")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Unique UUID v4 primary key for this farm profile."),
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="farms",
        db_index=True,
        help_text=_("User account (farmer/manager) that owns this farm."),
    )
    farm_name = models.CharField(
        _("farm name"),
        max_length=255,
        help_text=_("Descriptive name or title of the farm parcel."),
    )
    farm_image = models.ImageField(
        _("farm profile image"),
        upload_to="farms/%Y/%m/",
        blank=True,
        null=True,
    )
    area = models.DecimalField(
        _("total area"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Total surface area of the farm (must be greater than 0)."),
    )
    unit = models.CharField(
        _("area unit"),
        max_length=20,
        choices=AreaUnit.choices,
        default=AreaUnit.ACRES,
    )
    latitude = models.DecimalField(
        _("latitude"),
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text=_("GPS latitude coordinate ranging from -90.0 to 90.0."),
    )
    longitude = models.DecimalField(
        _("longitude"),
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text=_("GPS longitude coordinate ranging from -180.0 to 180.0."),
    )
    state = models.CharField(
        _("state / province"),
        max_length=100,
        blank=True,
    )
    district = models.CharField(
        _("district / county"),
        max_length=100,
        blank=True,
    )
    village = models.CharField(
        _("village / locality"),
        max_length=100,
        blank=True,
    )
    address = models.TextField(
        _("detailed physical address"),
        blank=True,
    )
    water_source = models.CharField(
        _("primary water source"),
        max_length=30,
        choices=WaterSource.choices,
        default=WaterSource.RAINFED,
    )
    status = models.CharField(
        _("operational status"),
        max_length=30,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
    )
    notes = models.TextField(
        _("additional notes"),
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
    active_objects = ActiveFarmManager()

    class Meta:
        verbose_name = _("farm")
        verbose_name_plural = _("farms")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "status", "is_deleted"]),
            models.Index(fields=["state", "district"]),
        ]

    def __str__(self) -> str:
        return f"{self.farm_name} ({self.owner.email})"

    def soft_delete(self) -> None:
        """Marks the farm instance as deleted without scrubbing database records."""
        self.is_deleted = True
        self.status = self.Status.ARCHIVED
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "status", "deleted_at", "updated_at"])

    def archive(self) -> None:
        """Transitions farm status to archived."""
        self.status = self.Status.ARCHIVED
        self.save(update_fields=["status", "updated_at"])
