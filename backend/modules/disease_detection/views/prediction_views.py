import logging
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from modules.disease_detection.models.prediction import DiseasePrediction
from modules.disease_detection.repositories.prediction_repository import (
    DiseasePredictionRepository,
)
from modules.disease_detection.serializers.prediction_serializers import (
    DiseasePredictionCreateSerializer,
    DiseasePredictionSerializer,
)
from modules.disease_detection.services.prediction_service import (
    DiseasePredictionService,
)

logger = logging.getLogger(__name__)

class DiseasePredictionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows disease predictions to be viewed or created.
    """

    serializer_class = DiseasePredictionSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        repo = DiseasePredictionRepository()
        return repo.get_user_predictions(self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return DiseasePredictionCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        logger.info(f"Received disease prediction request from user: {request.user.username}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = DiseasePredictionService()
        try:
            logger.info("Calling DiseasePredictionService.predict_disease...")
            prediction = service.predict_disease(
                user=request.user,
                image_file=serializer.validated_data["image"],
                farm=serializer.validated_data.get("farm"),
            )

            response_serializer = DiseasePredictionSerializer(prediction)
            logger.info(f"Successfully processed disease prediction: {prediction.id}")
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Failed to process disease prediction: {str(e)}")
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
