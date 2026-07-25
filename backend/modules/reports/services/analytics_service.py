from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
from modules.disease_detection.models.prediction import DiseasePrediction
from modules.crop_recommendation.models.recommendation import CropRecommendation

class AnalyticsService:
    def get_analytics(self, user):
        """
        Calculates trends, frequencies, and automatically generated insights.
        """
        now = timezone.now()
        six_months_ago = now - timedelta(days=180)
        
        # 1. Disease Frequency
        diseases_qs = DiseasePrediction.active_objects.filter(user=user, confidence_score__gte=0.6)
        disease_freq = list(diseases_qs.values('predicted_class')
                                       .annotate(count=Count('id'))
                                       .order_by('-count')[:10])
        
        # Clean up names
        for d in disease_freq:
            d['predicted_class'] = d['predicted_class'].replace('___', ' - ').replace('_', ' ')

        # 2. Monthly Scans Trend
        monthly_scans = list(DiseasePrediction.active_objects.filter(user=user, created_at__gte=six_months_ago)
                                        .annotate(month=TruncMonth('created_at'))
                                        .values('month')
                                        .annotate(count=Count('id'))
                                        .order_by('month'))
        
        # Format month for JSON
        for m in monthly_scans:
            m['month'] = m['month'].strftime('%b %Y')

        # 3. Auto-generated Insights
        insights = []
        if disease_freq:
            most_common = disease_freq[0]
            if 'healthy' not in most_common['predicted_class'].lower():
                insights.append(f"Your most frequently detected issue is {most_common['predicted_class']} ({most_common['count']} times). Consider applying preventative treatments across your fields.")
            else:
                insights.append(f"Great news! Your most frequent scan result is Healthy ({most_common['count']} times).")

        total_scans_last_month = sum([m['count'] for m in monthly_scans if m['month'] == now.strftime('%b %Y')])
        if total_scans_last_month > 10:
            insights.append("You have a high scan rate this month. Consistent monitoring helps catch diseases early.")
            
        crop_recs_count = CropRecommendation.active_objects.filter(user=user).count()
        if crop_recs_count == 0:
            insights.append("You haven't used the Crop Recommendation AI yet. Try it out to discover optimal crops for your soil.")

        return {
            "disease_frequency": disease_freq,
            "monthly_scans": monthly_scans,
            "insights": insights
        }
