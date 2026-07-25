"""Django AppConfig for Disease Diagnosis Module."""

from django.apps import AppConfig


class DiseaseDiagnosisConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.disease_diagnosis"
    verbose_name = "Disease Diagnosis Module"
