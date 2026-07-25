from rest_framework import serializers
from modules.disease_detection.models.prediction import DiseasePrediction

class DiseasePredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseasePrediction
        fields = [
            'id', 'user', 'farm', 'image', 'predicted_class', 
            'confidence_score', 'metadata', 'is_correct', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'predicted_class', 'confidence_score', 'metadata', 'created_at']

class DiseasePredictionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseasePrediction
        fields = ['image', 'farm']
        
    def validate_image(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("Image size cannot exceed 5MB.")
        return value
