#!/usr/bin/env python3
"""
Scaffolds the exact layered Modular Monolith directory and file skeleton
for all Dhatree AI backend feature modules.
"""
from pathlib import Path

MODULES = [
    ("users", "Users Module", "UsersConfig"),
    ("farms", "Farms Module", "FarmsConfig"),
    ("crop_recommendation", "Crop Recommendation Module", "CropRecommendationConfig"),
    ("disease_detection", "Disease Detection Module", "DiseaseDetectionConfig"),
    ("disease_diagnosis", "Disease Diagnosis Module", "DiseaseDiagnosisConfig"),
    ("soil_analysis", "Soil Analysis Module", "SoilAnalysisConfig"),
    ("fertilizer_recommendation", "Fertilizer Recommendation Module", "FertilizerRecommendationConfig"),
    ("weather_intelligence", "Weather Intelligence Module", "WeatherIntelligenceConfig"),
    ("notifications", "Notifications Module", "NotificationsConfig"),
    ("dashboard", "Dashboard Module", "DashboardConfig"),
    ("reports", "Reports Module", "ReportsConfig"),
]

LAYERS = ["models", "repositories", "services", "views", "serializers"]


def scaffold() -> None:
    root = Path(__file__).resolve().parent.parent / "backend" / "modules"
    for mod_name, verbose_name, config_class in MODULES:
        mod_path = root / mod_name
        mod_path.mkdir(parents=True, exist_ok=True)

        # __init__.py
        init_file = mod_path / "__init__.py"
        init_file.write_text(
            f'"""{verbose_name} domain boundary module."""\n'
            f'default_app_config = "modules.{mod_name}.apps.{config_class}"\n'
        )

        # apps.py
        apps_file = mod_path / "apps.py"
        apps_file.write_text(
            f'"""Django AppConfig for {verbose_name}."""\n'
            'from django.apps import AppConfig\n\n\n'
            f'class {config_class}(AppConfig):\n'
            '    default_auto_field = "django.db.models.BigAutoField"\n'
            f'    name = "modules.{mod_name}"\n'
            f'    verbose_name = "{verbose_name}"\n'
        )

        # urls.py
        urls_file = mod_path / "urls.py"
        urls_file.write_text(
            f'"""URL routing for {verbose_name}."""\n'
            'from django.urls import path\n\n'
            f'app_name = "{mod_name}"\n\n'
            'urlpatterns = [\n'
            f'    # API routes for {mod_name} (To be implemented in future phases)\n'
            ']\n'
        )

        # Sublayers
        for layer in LAYERS:
            layer_path = mod_path / layer
            layer_path.mkdir(parents=True, exist_ok=True)
            layer_init = layer_path / "__init__.py"
            layer_init.write_text(f'"""{verbose_name} {layer} package."""\n')

    print(f"Successfully scaffolded {len(MODULES)} backend feature modules.")


if __name__ == "__main__":
    scaffold()
