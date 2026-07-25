"""
SoilSample model definition.
Represents a soil test record for a specific farm.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class ActiveSoilSampleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoilSample(models.Model):
    """
    Soil test data for a farm parcel.
    """

    class Texture(models.TextChoices):
        SANDY = "sandy", _("Sandy")
        CLAY = "clay", _("Clay")
        SILT = "silt", _("Silt")
        LOAM = "loam", _("Loam")
        SANDY_LOAM = "sandy_loam", _("Sandy Loam")
        CLAY_LOAM = "clay_loam", _("Clay Loam")
        OTHER = "other", _("Other")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farm = models.ForeignKey(
        "farms.Farm",
        on_delete=models.CASCADE,
        related_name="soil_samples",
        help_text=_("Farm from which the sample was taken."),
    )
    sample_date = models.DateField(_("sample date"))

    nitrogen = models.DecimalField(
        _("nitrogen (N) mg/kg"), max_digits=8, decimal_places=2, blank=True, null=True
    )
    phosphorus = models.DecimalField(
        _("phosphorus (P) mg/kg"), max_digits=8, decimal_places=2, blank=True, null=True
    )
    potassium = models.DecimalField(
        _("potassium (K) mg/kg"), max_digits=8, decimal_places=2, blank=True, null=True
    )
    organic_carbon = models.DecimalField(
        _("organic carbon (%)"), max_digits=5, decimal_places=2, blank=True, null=True
    )
    ph_level = models.DecimalField(
        _("pH level"), max_digits=4, decimal_places=2, blank=True, null=True
    )
    moisture = models.DecimalField(
        _("moisture content (%)"), max_digits=5, decimal_places=2, blank=True, null=True
    )
    electrical_conductivity = models.DecimalField(
        _("electrical conductivity (dS/m)"),
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )
    texture = models.CharField(
        _("soil texture"), max_length=20, choices=Texture.choices, blank=True
    )

    remarks = models.TextField(_("remarks / lab notes"), blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    objects = models.Manager()
    active_objects = ActiveSoilSampleManager()

    class Meta:
        verbose_name = _("soil sample")
        verbose_name_plural = _("soil samples")
        ordering = ["-sample_date"]

    def __str__(self):
        return f"Soil Sample on {self.sample_date} for {self.farm.farm_name}"

    def soft_delete(self):
        self.is_deleted = True
        self.save(update_fields=["is_deleted", "updated_at"])
