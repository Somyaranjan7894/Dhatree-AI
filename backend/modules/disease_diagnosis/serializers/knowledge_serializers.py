from rest_framework import serializers
from modules.disease_diagnosis.models.knowledge import Disease, Treatment, Prevention, Reference

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = ['id', 'type', 'method', 'application_frequency', 'safety_precautions']

class PreventionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prevention
        fields = ['id', 'measure', 'timing']

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['id', 'source_name', 'url']

class DiseaseSerializer(serializers.ModelSerializer):
    treatments = TreatmentSerializer(many=True, read_only=True)
    preventions = PreventionSerializer(many=True, read_only=True)
    references = ReferenceSerializer(many=True, read_only=True)

    class Meta:
        model = Disease
        fields = [
            'id', 'name', 'crop', 'description', 'symptoms', 'possible_causes', 
            'severity', 'version', 'metadata', 'created_at', 'updated_at',
            'treatments', 'preventions', 'references'
        ]
