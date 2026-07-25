from rest_framework import serializers

from modules.crops.models.crop import Crop


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = [
            "id",
            "crop_name",
            "scientific_name",
            "season",
            "category",
            "duration_days",
            "description",
            "optimal_temp_min",
            "optimal_temp_max",
            "optimal_rainfall_min",
            "optimal_rainfall_max",
            "optimal_humidity_min",
            "optimal_humidity_max",
            "optimal_ph_min",
            "optimal_ph_max",
            "water_requirement",
            "growth_stages",
            "created_at",
            "updated_at",
        ]
