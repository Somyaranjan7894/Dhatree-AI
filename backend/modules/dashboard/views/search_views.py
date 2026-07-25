from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from core.permissions import IsAuthenticated
from core.responses import success_response
from modules.dashboard.services.search_service import GlobalSearchService

class GlobalSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(description="Perform a global fuzzy search across the platform.")
    def get(self, request: Request) -> Response:
        query = request.query_params.get("q", "")
        service = GlobalSearchService()
        data = service.search(user=request.user, query=query)
        return success_response(data=data, message="Search completed successfully.")
