"""
Crop model definition for Dhatree AI Agriculture Platform.
Represents global master data for crops.
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class ActiveCropManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Crop(models.Model):
    """
    Global master directory of crops.
    """
    class Season(models.TextChoices):
        KHARIF = "kharif", _("Kharif (Monsoon)")
        RABI = "rabi", _("Rabi (Winter)")
        ZAID = "zaid", _("Zaid (Summer)")
        ALL_SEASON = "all_season", _("All Season")

    class Category(models.TextChoices):
        CEREAL = "cereal", _("Cereal")
        PULSE = "pulse", _("Pulse")
        OILSEED = "oilseed", _("Oilseed")
        VEGETABLE = "vegetable", _("Vegetable")
        FRUIT = "fruit", _("Fruit")
        FIBER = "fiber", _("Fiber")
        SPICE = "spice", _("Spice")
        OTHER = "other", _("Other")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    crop_name = models.CharField(_("crop name"), max_length=100, unique=True)
    scientific_name = models.CharField(_("scientific name"), max_length=150, blank=True)
    season = models.CharField(
        _("growing season"),
        max_length=20,
        choices=Season.choices,
        default=Season.ALL_SEASON,
    )
    category = models.CharField(
        _("crop category"),
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
    )
    duration_days = models.PositiveIntegerField(
        _("typical duration in days"),
        blank=True,
        null=True,
    )
    description = models.TextField(_("description"), blank=True)
    
    # Optimal Ranges
    optimal_temp_min = models.DecimalField(_("optimal min temperature (°C)"), max_digits=5, decimal_places=2, blank=True, null=True)
    optimal_temp_max = models.DecimalField(_("optimal max temperature (°C)"), max_digits=5, decimal_places=2, blank=True, null=True)
    optimal_rainfall_min = models.DecimalField(_("optimal min rainfall (mm)"), max_digits=6, decimal_places=2, blank=True, null=True)
    optimal_rainfall_max = models.DecimalField(_("optimal max rainfall (mm)"), max_digits=6, decimal_places=2, blank=True, null=True)
    optimal_humidity_min = models.DecimalField(_("optimal min humidity (%)"), max_digits=5, decimal_places=2, blank=True, null=True)
    optimal_humidity_max = models.DecimalField(_("optimal max humidity (%)"), max_digits=5, decimal_places=2, blank=True, null=True)
    optimal_ph_min = models.DecimalField(_("optimal min pH"), max_digits=4, decimal_places=2, blank=True, null=True)
    optimal_ph_max = models.DecimalField(_("optimal max pH"), max_digits=4, decimal_places=2, blank=True, null=True)
    
    water_requirement = models.TextField(_("water requirement description"), blank=True)
    growth_stages = models.JSONField(_("growth stages"), default=list, blank=True, help_text=_("JSON list of growth stages"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    objects = models.Manager()
    active_objects = ActiveCropManager()

    class Meta:
        verbose_name = _("crop")
        verbose_name_plural = _("crops")
        ordering = ["crop_name"]

    def __str__(self):
        return self.crop_name

    def soft_delete(self):
        self.is_deleted = True
        self.save(update_fields=["is_deleted", "updated_at"])
