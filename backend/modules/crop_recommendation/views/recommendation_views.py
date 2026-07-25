from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from modules.crop_recommendation.services.recommendation_service import CropRecommendationService
from modules.crop_recommendation.serializers.recommendation_serializers import CropRecommendationSerializer, CropRecommendationCreateSerializer

class CropRecommendationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def create(self, request):
        serializer = CropRecommendationCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        service = CropRecommendationService()
        try:
            prediction = service.predict_crop(
                user=request.user,
                data=serializer.validated_data,
                farm=serializer.validated_data.get('farm')
            )
            response_serializer = CropRecommendationSerializer(prediction)
            return Response({
                "status": "success",
                "data": response_serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        service = CropRecommendationService()
        history = service.repository.get_user_recommendations(user=request.user)
        serializer = CropRecommendationSerializer(history, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
