"""Django AppConfig for Farms Module."""

from django.apps import AppConfig


class FarmsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.farms"
    verbose_name = "Farms Module"
