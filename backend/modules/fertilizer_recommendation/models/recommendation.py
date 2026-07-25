import uuid
from django.db import models
from django.conf import settings
from modules.farms.models import Farm

class FertilizerRecommendation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="fertilizer_recommendations")
    farm = models.ForeignKey(Farm, on_delete=models.SET_NULL, null=True, blank=True, related_name="fertilizer_recommendations")
    
    # Inputs
    crop_type = models.CharField(max_length=100)
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    ph_level = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()
    soil_type = models.CharField(max_length=100, blank=True, null=True)
    
    # Outputs
    recommended_fertilizer = models.CharField(max_length=100)
    confidence_score = models.FloatField(default=1.0)
    explanation = models.TextField(blank=True, null=True)
    application_guidance = models.TextField(blank=True, null=True)
    warnings = models.TextField(blank=True, null=True)
    
    # Metadata (for alternative predictions, model version, etc)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Audit
    is_correct = models.BooleanField(null=True, blank=True) # For user feedback
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "ai_fertilizer_recommendations"
        ordering = ["-created_at"]
        
    def __str__(self):
        return f"{self.recommended_fertilizer} for {self.crop_type} ({self.created_at.date()})"
