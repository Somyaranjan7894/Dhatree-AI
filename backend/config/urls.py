"""
Dhatree AI Root URL Configuration.
Maps API routes to independent domain modules inside `modules/`.
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from core.views.health_views import LivenessView, ReadinessView

urlpatterns = [
    # Django Admin Interface
    path("admin/", admin.site.urls),
    # Health checks
    path("api/health/liveness/", LivenessView.as_view(), name="liveness"),
    path("api/health/readiness/", ReadinessView.as_view(), name="readiness"),
    # OpenAPI Specification & Swagger Documentation
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/v1/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Modular Monolith API v1 Endpoints
    path(
        "api/v1/auth/",
        include("modules.authentication.urls", namespace="authentication"),
    ),
    path("api/v1/users/", include("modules.users.urls", namespace="users")),
    path("api/v1/farms/", include("modules.farms.urls", namespace="farms")),
    path("api/v1/crops/", include("modules.crops.urls", namespace="crops")),
    path(
        "api/v1/crop-recommendation/",
        include("modules.crop_recommendation.urls", namespace="crop_recommendation"),
    ),
    path(
        "api/v1/disease-detection/",
        include("modules.disease_detection.urls", namespace="disease_detection"),
    ),
    path(
        "api/v1/disease-diagnosis/",
        include("modules.disease_diagnosis.urls", namespace="disease_diagnosis"),
    ),
    path(
        "api/v1/soil-analysis/",
        include("modules.soil_analysis.urls", namespace="soil_analysis"),
    ),
    path(
        "api/v1/fertilizer-recommendation/",
        include(
            "modules.fertilizer_recommendation.urls",
            namespace="fertilizer_recommendation",
        ),
    ),
    path(
        "api/v1/weather-intelligence/",
        include("modules.weather_intelligence.urls", namespace="weather_intelligence"),
    ),
    path(
        "api/v1/notifications/",
        include("modules.notifications.urls", namespace="notifications"),
    ),
    path(
        "api/v1/dashboard/",
        include("modules.dashboard.urls", namespace="dashboard"),
    ),
    path(
        "api/v1/assistant/",
        include("modules.ai_assistant.urls", namespace="ai_assistant"),
    ),
    path("api/v1/reports/", include("modules.reports.urls", namespace="reports")),
]
