import uuid

from django.conf import settings
from django.db import models


class CropRecommendation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="crop_recommendations",
    )
    farm = models.ForeignKey(
        "farms.Farm",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="crop_recommendations",
    )

    # Input features
    nitrogen = models.FloatField()
    phosphorus = models.FloatField()
    potassium = models.FloatField()
    ph = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()

    # Output
    recommended_crop = models.CharField(max_length=100)
    confidence_score = models.FloatField()
    alternatives = models.JSONField(default=list, blank=True)
    explanation = models.TextField(blank=True)

    # Metadata
    model_version = models.CharField(max_length=50, default="v1.0")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ai_crop_recommendations"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.user.email} - {self.recommended_crop} ({self.confidence_score:.2f})"
        )
