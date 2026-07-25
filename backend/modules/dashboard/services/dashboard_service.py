from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from modules.crop_recommendation.models.recommendation import CropRecommendation
from modules.disease_detection.models.prediction import DiseasePrediction
from modules.farms.models.farm import Farm
from modules.fertilizer_recommendation.models.recommendation import (
    FertilizerRecommendation,
)
from modules.notifications.models.notification import Notification


class DashboardService:
    def get_dashboard_overview(self, user):
        """
        Returns actionable insights and overview data for the Smart Farmer Dashboard.
        """
        now = timezone.now()
        last_month = now - timedelta(days=30)

        # Farm metrics
        active_farms = Farm.active_objects.filter(owner=user).count()

        # Prediction counts
        disease_predictions_count = DiseasePrediction.objects.filter(user=user).count()
        recent_diseases = (
            DiseasePrediction.objects.filter(user=user, confidence_score__gte=0.7)
            .exclude(predicted_class__icontains="healthy")
            .order_by("-created_at")[:5]
        )

        # Recommendations
        recent_crop_recs = CropRecommendation.objects.filter(user=user).order_by(
            "-created_at"
        )[:5]
        recent_fert_recs = FertilizerRecommendation.objects.filter(user=user).order_by(
            "-created_at"
        )[:5]

        # Notifications (Actionable Tasks)
        actionable_notifications = Notification.objects.filter(
            user=user,
            is_read=False,
            notification_type__in=[
                Notification.NotificationType.WARNING,
                Notification.NotificationType.CRITICAL,
            ],
        ).order_by("-created_at")[:5]

        # Actionable insights generation
        insights = []
        if active_farms == 0:
            insights.append(
                {
                    "type": "info",
                    "message": "You haven't added any farms yet. Add a farm to start receiving tailored insights.",
                }
            )

        if recent_diseases.exists():
            latest = recent_diseases.first()
            disease_name = latest.predicted_class.replace("___", " - ").replace(
                "_", " "
            )
            insights.append(
                {
                    "type": "warning",
                    "message": f"Action needed: We recently detected {disease_name}. Check the treatment plan.",
                }
            )

        if actionable_notifications.exists():
            insights.append(
                {
                    "type": "critical",
                    "message": f"You have {actionable_notifications.count()} unread alerts that need your attention.",
                }
            )

        return {
            "metrics": {
                "active_farms": active_farms,
                "total_disease_predictions": disease_predictions_count,
                "unread_alerts": actionable_notifications.count(),
            },
            "insights": insights,
            "recent_activity": {
                "diseases": [
                    {
                        "id": str(d.id),
                        "disease": d.predicted_class,
                        "confidence": d.confidence_score,
                        "date": d.created_at,
                    }
                    for d in recent_diseases
                ],
                "crop_recommendations": [
                    {
                        "id": str(c.id),
                        "crop": c.recommended_crop,
                        "confidence": c.confidence_score,
                        "date": c.created_at,
                    }
                    for c in recent_crop_recs
                ],
                "fertilizer_recommendations": [
                    {
                        "id": str(f.id),
                        "crop": f.crop_type,
                        "fertilizer": f.recommended_fertilizer,
                        "date": f.created_at,
                    }
                    for f in recent_fert_recs
                ],
            },
        }
