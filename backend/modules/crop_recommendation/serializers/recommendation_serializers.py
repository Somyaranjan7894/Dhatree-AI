from rest_framework import serializers

from modules.crop_recommendation.models.recommendation import CropRecommendation
from modules.farms.models.farm import Farm


class CropRecommendationCreateSerializer(serializers.Serializer):
    farm = serializers.PrimaryKeyRelatedField(
        queryset=Farm.objects.all(), required=False, allow_null=True
    )
    nitrogen = serializers.FloatField(min_value=0, max_value=300)
    phosphorus = serializers.FloatField(min_value=0, max_value=300)
    potassium = serializers.FloatField(min_value=0, max_value=300)
    ph = serializers.FloatField(min_value=0, max_value=14)
    temperature = serializers.FloatField(min_value=-20, max_value=60)
    humidity = serializers.FloatField(min_value=0, max_value=100)
    rainfall = serializers.FloatField(min_value=0, max_value=1000)


class CropRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropRecommendation
        fields = "__all__"
        read_only_fields = [
            "id",
            "user",
            "recommended_crop",
            "confidence_score",
            "alternatives",
            "explanation",
            "model_version",
            "created_at",
        ]
