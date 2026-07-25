"""
URL routes for User domain module (`/api/v1/users/`).
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from modules.users.views.user_views import UserViewSet

app_name = "users"

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
