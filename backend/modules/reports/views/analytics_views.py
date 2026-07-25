from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from core.permissions import IsAuthenticated
from core.responses import success_response
from modules.reports.services.analytics_service import AnalyticsService

class AnalyticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(description="Get analytics and auto-generated insights.")
    def get(self, request: Request) -> Response:
        service = AnalyticsService()
        data = service.get_analytics(user=request.user)
        return success_response(data=data, message="Analytics retrieved successfully.")
