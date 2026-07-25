"""Django AppConfig for Weather Intelligence Module."""
from django.apps import AppConfig


class WeatherIntelligenceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.weather_intelligence"
    verbose_name = "Weather Intelligence Module"
