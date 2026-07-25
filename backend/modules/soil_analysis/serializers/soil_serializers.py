from rest_framework import serializers

from modules.soil_analysis.models.soil_sample import SoilSample


class SoilSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoilSample
        fields = [
            "id",
            "farm",
            "sample_date",
            "nitrogen",
            "phosphorus",
            "potassium",
            "organic_carbon",
            "ph_level",
            "moisture",
            "electrical_conductivity",
            "texture",
            "remarks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["farm"]
