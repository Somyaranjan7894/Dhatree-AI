import json

from django.core.management.base import BaseCommand

from modules.disease_diagnosis.models.knowledge import (
    Disease,
    Prevention,
    Reference,
    Treatment,
)


class Command(BaseCommand):
    help = "Seeds the Disease Diagnosis Knowledge Base with initial data"

    def handle(self, *args, **kwargs):
        import os

        json_path = os.path.join(os.path.dirname(__file__), "disease_seed_data.json")
        with open(json_path, "r") as f:
            seed_data = json.load(f)

        created_count = 0
        for d_data in seed_data:
            disease, created = Disease.objects.get_or_create(
                name=d_data["name"],
                defaults={
                    "crop": d_data["crop"],
                    "description": d_data["description"],
                    "symptoms": d_data["symptoms"],
                    "severity": d_data["severity"],
                    "version": "1.0.0",
                },
            )

            if created:
                created_count += 1
                for t in d_data.get("treatments", []):
                    Treatment.objects.create(disease=disease, **t)
                for p in d_data.get("preventions", []):
                    Prevention.objects.create(disease=disease, **p)
                for r in d_data.get("references", []):
                    Reference.objects.create(disease=disease, **r)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully seeded {created_count} new diseases.")
        )
