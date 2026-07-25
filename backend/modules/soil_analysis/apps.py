"""Django AppConfig for Soil Analysis Module."""
from django.apps import AppConfig


class SoilAnalysisConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.soil_analysis"
    verbose_name = "Soil Analysis Module"
