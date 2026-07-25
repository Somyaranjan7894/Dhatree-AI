import uuid

from django.conf import settings
from django.db import models

from modules.farms.models.farm import Farm


class DiseasePrediction(models.Model):
    """
    Records the outcome of a crop disease prediction.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="disease_predictions",
    )
    farm = models.ForeignKey(
        Farm,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="disease_predictions",
    )

    # Store the image. Requires MEDIA_ROOT to be configured.
    image = models.ImageField(upload_to="disease_images/%Y/%m/%d/")

    # AI Engine Outputs
    predicted_class = models.CharField(max_length=255)
    confidence_score = models.FloatField()
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text="Stores top predictions, grad-cam heatmap, and model version",
    )

    # Meta
    is_correct = models.BooleanField(
        null=True, blank=True, help_text="User feedback if prediction was correct"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ai_disease_predictions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.predicted_class} ({self.confidence_score*100:.1f}%) by {self.user.email}"
