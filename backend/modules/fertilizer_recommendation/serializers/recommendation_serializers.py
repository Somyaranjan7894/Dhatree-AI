from rest_framework import serializers
from modules.fertilizer_recommendation.models.recommendation import FertilizerRecommendation

class FertilizerRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FertilizerRecommendation
        fields = [
            'id', 'user', 'farm', 'crop_type', 'nitrogen', 'phosphorus', 'potassium',
            'ph_level', 'temperature', 'humidity', 'rainfall', 'soil_type',
            'recommended_fertilizer', 'confidence_score', 'explanation',
            'application_guidance', 'warnings', 'metadata', 'is_correct', 'created_at'
        ]
        read_only_fields = [
            'id', 'user', 'recommended_fertilizer', 'confidence_score',
            'explanation', 'application_guidance', 'warnings', 'metadata', 'created_at'
        ]

class FertilizerPredictionRequestSerializer(serializers.Serializer):
    farm = serializers.UUIDField(required=False, allow_null=True)
    crop_type = serializers.CharField(max_length=100)
    nitrogen = serializers.FloatField(min_value=0, max_value=500)
    phosphorus = serializers.FloatField(min_value=0, max_value=500)
    potassium = serializers.FloatField(min_value=0, max_value=500)
    ph_level = serializers.FloatField(min_value=0, max_value=14)
    temperature = serializers.FloatField(min_value=-50, max_value=60)
    humidity = serializers.FloatField(min_value=0, max_value=100)
    rainfall = serializers.FloatField(min_value=0, max_value=5000)
    soil_type = serializers.CharField(max_length=100, required=False, allow_blank=True)
    confidence_threshold = serializers.FloatField(min_value=0.0, max_value=1.0, required=False, default=0.5)
