"""
URL routes for Authentication domain module (`/api/v1/auth/`).
"""
from django.urls import path
from modules.authentication.views.auth_views import (
    ChangePasswordAPIView,
    CurrentUserAPIView,
    ForgotPasswordAPIView,
    LoginAPIView,
    LogoutAPIView,
    ProfileUpdateAPIView,
    RefreshTokenAPIView,
    RegisterAPIView,
    ResetPasswordAPIView,
    VerifyEmailAPIView,
    VerifyTokenAPIView,
)

app_name = "authentication"

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("refresh/", RefreshTokenAPIView.as_view(), name="refresh"),
    path("verify/", VerifyTokenAPIView.as_view(), name="verify"),
    path("me/", CurrentUserAPIView.as_view(), name="me"),
    path("profile/", ProfileUpdateAPIView.as_view(), name="profile"),
    path("change-password/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("forgot-password/", ForgotPasswordAPIView.as_view(), name="forgot-password"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset-password"),
    path("verify-email/", VerifyEmailAPIView.as_view(), name="verify-email"),
]
