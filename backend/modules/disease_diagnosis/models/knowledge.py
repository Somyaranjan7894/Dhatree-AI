import uuid

from django.db import models


class Disease(models.Model):
    SEVERITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Common name or technical name of the disease (e.g. Apple___Apple_scab)",
    )
    crop = models.CharField(max_length=100, db_index=True)
    description = models.TextField()
    symptoms = models.TextField(help_text="Detailed symptoms of the disease")
    possible_causes = models.TextField(blank=True, null=True)
    severity = models.CharField(
        max_length=20, choices=SEVERITY_CHOICES, default="Medium"
    )

    # Versioning & Metadata
    version = models.CharField(max_length=50, default="1.0.0")
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ai_knowledge_disease"
        ordering = ["crop", "name"]

    def __str__(self):
        return f"{self.crop} - {self.name}"


class Treatment(models.Model):
    TREATMENT_TYPES = [
        ("Organic", "Organic"),
        ("Chemical", "Chemical"),
        ("Biological", "Biological"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    disease = models.ForeignKey(
        Disease, on_delete=models.CASCADE, related_name="treatments"
    )
    type = models.CharField(max_length=50, choices=TREATMENT_TYPES)
    method = models.TextField()
    application_frequency = models.CharField(max_length=100, blank=True, null=True)
    safety_precautions = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "ai_knowledge_treatment"

    def __str__(self):
        return f"{self.type} Treatment for {self.disease.name}"


class Prevention(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    disease = models.ForeignKey(
        Disease, on_delete=models.CASCADE, related_name="preventions"
    )
    measure = models.TextField()
    timing = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="e.g. Pre-planting, Post-harvest",
    )

    class Meta:
        db_table = "ai_knowledge_prevention"

    def __str__(self):
        return f"Prevention for {self.disease.name}"


class Reference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    disease = models.ForeignKey(
        Disease, on_delete=models.CASCADE, related_name="references"
    )
    source_name = models.CharField(max_length=255)
    url = models.URLField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = "ai_knowledge_reference"

    def __str__(self):
        return f"Source: {self.source_name}"
