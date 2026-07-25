from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from modules.fertilizer_recommendation.models.recommendation import (
    FertilizerRecommendation,
)
from modules.fertilizer_recommendation.serializers.recommendation_serializers import (
    FertilizerPredictionRequestSerializer,
    FertilizerRecommendationSerializer,
)
from modules.fertilizer_recommendation.services.recommendation_service import (
    FertilizerRecommendationService,
)


class FertilizerRecommendationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FertilizerRecommendationSerializer

    def get_queryset(self):
        return FertilizerRecommendation.objects.filter(user=self.request.user)

    @extend_schema(
        request=FertilizerPredictionRequestSerializer,
        responses={201: FertilizerRecommendationSerializer},
        description="Predict the best fertilizer based on soil and weather parameters.",
    )
    def create(self, request, *args, **kwargs):
        req_serializer = FertilizerPredictionRequestSerializer(data=request.data)
        req_serializer.is_valid(raise_exception=True)

        try:
            recommendation = FertilizerRecommendationService.predict_fertilizer(
                user=request.user, data=req_serializer.validated_data
            )
            resp_serializer = self.get_serializer(recommendation)
            return Response(resp_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
