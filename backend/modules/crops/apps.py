"""Django AppConfig for Crops Module (`modules.crops`)."""

from django.apps import AppConfig


class CropsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.crops"
    label = "crops"
    verbose_name = "Crops Master Module"
