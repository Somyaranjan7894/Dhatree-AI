import logging
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from modules.crop_recommendation.serializers.recommendation_serializers import (
    CropRecommendationCreateSerializer,
    CropRecommendationSerializer,
)
from modules.crop_recommendation.services.recommendation_service import (
    CropRecommendationService,
)

logger = logging.getLogger(__name__)


class CropRecommendationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        logger.info(f"Received crop recommendation request from user: {request.user.username}")
        serializer = CropRecommendationCreateSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Invalid crop recommendation payload: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        service = CropRecommendationService()
        try:
            logger.info("Calling CropRecommendationService.predict_crop...")
            prediction = service.predict_crop(
                user=request.user,
                data=serializer.validated_data,
                farm=serializer.validated_data.get("farm"),
            )
            response_serializer = CropRecommendationSerializer(prediction)
            logger.info(f"Successfully processed crop recommendation. Suggested crop: {prediction.recommended_crop}")
            return Response(
                {"status": "success", "data": response_serializer.data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            logger.error(f"Failed to process crop recommendation: {str(e)}\n{error_trace}")
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def list(self, request):
        service = CropRecommendationService()
        history = service.repository.get_user_recommendations(user=request.user)
        serializer = CropRecommendationSerializer(history, many=True)
        return Response(
            {"status": "success", "data": serializer.data}, status=status.HTTP_200_OK
        )
