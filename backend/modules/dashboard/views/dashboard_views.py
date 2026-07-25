from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsAuthenticated
from core.responses import success_response
from modules.dashboard.services.dashboard_service import DashboardService


class DashboardOverviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Get actionable insights and overview data for the user dashboard."
    )
    # @method_decorator(cache_page(60 * 5)) # Cache for 5 minutes - optional optimization
    def get(self, request: Request) -> Response:
        service = DashboardService()
        data = service.get_dashboard_overview(user=request.user)
        return success_response(
            data=data, message="Dashboard overview retrieved successfully."
        )
