from django.core.management.base import BaseCommand
from modules.disease_diagnosis.models.knowledge import Disease, Treatment, Prevention, Reference
import json

class Command(BaseCommand):
    help = 'Seeds the Disease Diagnosis Knowledge Base with initial data'

    def handle(self, *args, **kwargs):
        # A small mock seed list of diseases often found in PlantVillage
        seed_data = [
            {
                "name": "Apple___Apple_scab",
                "crop": "Apple",
                "description": "Apple scab is a disease of Malus trees, such as apple trees, caused by the ascomycete fungus Venturia inaequalis.",
                "symptoms": "Dull black or grey-brown lesions on the surface of tree leaves, buds or fruits.",
                "severity": "Medium",
                "treatments": [
                    {
                        "type": "Chemical",
                        "method": "Apply fungicides like Captan or Mancozeb.",
                        "application_frequency": "Every 7-10 days starting from green tip stage until petal fall.",
                        "safety_precautions": "Wear protective clothing and mask during application."
                    },
                    {
                        "type": "Organic",
                        "method": "Apply Neem oil or liquid copper soap.",
                        "application_frequency": "Every 7 days during early spring.",
                        "safety_precautions": "Avoid application in temperatures over 85°F."
                    }
                ],
                "preventions": [
                    {
                        "measure": "Rake and destroy fallen leaves in autumn.",
                        "timing": "Autumn/Winter"
                    },
                    {
                        "measure": "Prune trees to allow better air circulation.",
                        "timing": "Winter"
                    }
                ],
                "references": [
                    {
                        "source_name": "Agricultural Extension Service",
                        "url": "https://example.com/apple-scab"
                    }
                ]
            },
            {
                "name": "Corn___Common_rust",
                "crop": "Corn",
                "description": "Common rust is a fungal disease affecting corn caused by Puccinia sorghi.",
                "symptoms": "Small, round to elongate, cinnamon-brown pustules on both surfaces of the leaves.",
                "severity": "Low",
                "treatments": [
                    {
                        "type": "Chemical",
                        "method": "Apply foliar fungicides containing strobilurins or triazoles.",
                        "application_frequency": "At the first sign of pustules.",
                        "safety_precautions": "Do not apply near water sources."
                    }
                ],
                "preventions": [
                    {
                        "measure": "Use rust-resistant corn hybrids.",
                        "timing": "Pre-planting"
                    }
                ],
                "references": []
            },
            {
                "name": "Potato___Late_blight",
                "crop": "Potato",
                "description": "Late blight is a devastating disease of potato caused by Phytophthora infestans.",
                "symptoms": "Water-soaked lesions on leaves that turn brown/black, white fungal growth in high humidity.",
                "severity": "Critical",
                "treatments": [
                    {
                        "type": "Chemical",
                        "method": "Apply Chlorothalonil or Mancozeb immediately.",
                        "application_frequency": "Every 5-7 days under wet conditions.",
                        "safety_precautions": "Toxic to aquatic life; follow label strictly."
                    }
                ],
                "preventions": [
                    {
                        "measure": "Destroy cull piles and volunteers.",
                        "timing": "Spring"
                    }
                ],
                "references": []
            }
        ]

        created_count = 0
        for d_data in seed_data:
            disease, created = Disease.objects.get_or_create(
                name=d_data['name'],
                defaults={
                    'crop': d_data['crop'],
                    'description': d_data['description'],
                    'symptoms': d_data['symptoms'],
                    'severity': d_data['severity'],
                    'version': '1.0.0'
                }
            )
            
            if created:
                created_count += 1
                for t in d_data.get('treatments', []):
                    Treatment.objects.create(disease=disease, **t)
                for p in d_data.get('preventions', []):
                    Prevention.objects.create(disease=disease, **p)
                for r in d_data.get('references', []):
                    Reference.objects.create(disease=disease, **r)

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {created_count} new diseases.'))
