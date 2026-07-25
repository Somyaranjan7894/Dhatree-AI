from rest_framework import serializers
from modules.weather_intelligence.models.weather_snapshot import WeatherSnapshot

class WeatherSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherSnapshot
        fields = [
            "id",
            "farm",
            "date",
            "temperature",
            "humidity",
            "rainfall",
            "wind_speed",
            "pressure",
            "cloud_cover",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["farm"]
