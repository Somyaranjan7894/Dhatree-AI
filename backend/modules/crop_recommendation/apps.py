"""Django AppConfig for Crop Recommendation Module."""

from django.apps import AppConfig


class CropRecommendationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.crop_recommendation"
    verbose_name = "Crop Recommendation Module"
