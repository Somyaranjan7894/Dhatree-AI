"""Django AppConfig for Disease Detection Module."""
from django.apps import AppConfig


class DiseaseDetectionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.disease_detection"
    verbose_name = "Disease Detection Module"
