from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db import connection
from drf_spectacular.utils import extend_schema

class LivenessView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(description="Check if the application is running.", tags=["Health"])
    def get(self, request: Request) -> Response:
        return Response({"status": "ok"}, status=200)

class ReadinessView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(description="Check if the application is ready to receive traffic.", tags=["Health"])
    def get(self, request: Request) -> Response:
        health_status = {
            "status": "ok",
            "database": "unknown"
        }
        try:
            connection.ensure_connection()
            health_status["database"] = "ok"
        except Exception as e:
            health_status["database"] = "failed"
            health_status["status"] = "error"
            return Response(health_status, status=503)
            
        return Response(health_status, status=200)
