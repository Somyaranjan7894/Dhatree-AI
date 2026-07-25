from django.db.models.signals import post_save
from django.dispatch import receiver

from modules.crop_recommendation.models.recommendation import CropRecommendation
from modules.disease_detection.models.prediction import DiseasePrediction
from modules.fertilizer_recommendation.models.recommendation import (
    FertilizerRecommendation,
)

from .models.notification import Notification


@receiver(post_save, sender=DiseasePrediction)
def create_disease_prediction_notification(sender, instance, created, **kwargs):
    if created:
        cat = Notification.NotificationCategory.PREDICTION
        ntype = Notification.NotificationType.INFORMATION

        disease_name = instance.predicted_class.replace("___", " - ").replace("_", " ")

        if "healthy" in instance.predicted_class.lower():
            title = "Crop is Healthy"
            desc = f"Your crop scan indicates it is healthy with {(instance.confidence_score*100):.1f}% confidence."
            ntype = Notification.NotificationType.SUCCESS
        elif instance.confidence_score < 0.6:
            title = "Low Confidence Disease Prediction"
            desc = f"We detected a possible issue ({disease_name}) but with low confidence ({(instance.confidence_score*100):.1f}%). Please review manually."
            ntype = Notification.NotificationType.WARNING
            cat = Notification.NotificationCategory.ALERT
        else:
            title = f"Disease Detected: {disease_name}"
            desc = f"Disease detected with {(instance.confidence_score*100):.1f}% confidence. Please check the diagnosis details for treatment plans."
            ntype = Notification.NotificationType.WARNING

        Notification.objects.create(
            user=instance.user,
            title=title,
            description=desc,
            notification_type=ntype,
            category=cat,
        )


@receiver(post_save, sender=CropRecommendation)
def create_crop_rec_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            title="New Crop Recommendation Ready",
            description=f"Based on your soil data, we recommend planting {instance.recommended_crop} ({(instance.confidence_score*100):.1f}% confidence).",
            notification_type=Notification.NotificationType.SUCCESS,
            category=Notification.NotificationCategory.RECOMMENDATION,
        )


@receiver(post_save, sender=FertilizerRecommendation)
def create_fert_rec_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            title="New Fertilizer Plan Ready",
            description=f"Your customized fertilizer plan for {instance.crop_type} is ready: {instance.recommended_fertilizer}.",
            notification_type=Notification.NotificationType.SUCCESS,
            category=Notification.NotificationCategory.RECOMMENDATION,
        )
