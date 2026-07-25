"""
WeatherSnapshot model definition.
Represents a recorded weather condition for a farm at a specific time.
"""

import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class ActiveWeatherSnapshotManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class WeatherSnapshot(models.Model):
    """
    Weather data snapshot for a specific farm on a specific date.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farm = models.ForeignKey(
        "farms.Farm",
        on_delete=models.CASCADE,
        related_name="weather_snapshots",
        help_text=_("Farm this weather snapshot belongs to."),
    )
    date = models.DateTimeField(_("snapshot date and time"))

    temperature = models.DecimalField(
        _("temperature (°C)"), max_digits=5, decimal_places=2, blank=True, null=True
    )
    humidity = models.DecimalField(
        _("humidity (%)"), max_digits=5, decimal_places=2, blank=True, null=True
    )
    rainfall = models.DecimalField(
        _("rainfall (mm)"), max_digits=6, decimal_places=2, blank=True, null=True
    )
    wind_speed = models.DecimalField(
        _("wind speed (km/h)"), max_digits=5, decimal_places=2, blank=True, null=True
    )
    pressure = models.DecimalField(
        _("atmospheric pressure (hPa)"),
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
    )
    cloud_cover = models.DecimalField(
        _("cloud cover (%)"), max_digits=5, decimal_places=2, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    objects = models.Manager()
    active_objects = ActiveWeatherSnapshotManager()

    class Meta:
        verbose_name = _("weather snapshot")
        verbose_name_plural = _("weather snapshots")
        ordering = ["-date"]

    def __str__(self):
        return f"Weather Snapshot for {self.farm.farm_name} at {self.date}"

    def soft_delete(self):
        self.is_deleted = True
        self.save(update_fields=["is_deleted", "updated_at"])
