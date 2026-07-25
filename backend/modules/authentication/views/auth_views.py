"""
API Views for Authentication and Account Lifecycle.
Strictly decoupled from data access and business logic via AuthService and UserService.
"""

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsAuthenticated
from core.responses import success_response
from modules.authentication.serializers.auth_serializers import (
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    LogoutSerializer,
    RefreshTokenSerializer,
    RegisterSerializer,
    ResetPasswordSerializer,
    VerifyEmailSerializer,
)
from modules.authentication.services.auth_service import AuthService
from modules.users.serializers.user_serializers import (
    UserSerializer,
    UserUpdateSerializer,
)
from modules.users.services.user_service import UserService


class RegisterAPIView(APIView):
    """Endpoint for user account registration (`POST /api/v1/auth/register/`)."""

    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    @extend_schema(
        request=RegisterSerializer,
        summary="Register a new user account.",
        description="Creates a new account, hashes credentials, and returns initial JWT tokens alongside the profile.",
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = AuthService()
        user, tokens = auth_service.register(**serializer.validated_data)

        data = {
            "user": UserSerializer(user).data,
            "tokens": tokens,
        }
        return success_response(
            data=data,
            message="User account registered successfully.",
            status_code=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    """Endpoint for user login (`POST /api/v1/auth/login/`)."""

    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        summary="Log in with email or username.",
        description="Verifies user credentials and account active status, returning JWT tokens and user details.",
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = AuthService()
        user, tokens = auth_service.login(
            identifier=serializer.validated_data["identifier"],
            password=serializer.validated_data["password"],
        )

        data = {
            "user": UserSerializer(user).data,
            "tokens": tokens,
        }
        return success_response(data=data, message="Logged in successfully.")


class LogoutAPIView(APIView):
    """Endpoint for user logout and token blacklisting (`POST /api/v1/auth/logout/`)."""

    permission_classes = [AllowAny]
    serializer_class = LogoutSerializer

    @extend_schema(
        request=LogoutSerializer,
        summary="Log out and blacklist refresh token.",
        description="Blacklists the provided refresh token so it cannot be used to issue further access tokens.",
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = AuthService()
        auth_service.logout(refresh_token_str=serializer.validated_data["refresh"])

        return success_response(
            data={}, message="Logged out and token blacklisted successfully."
        )


class RefreshTokenAPIView(APIView):
    """Endpoint for token rotation (`POST /api/v1/auth/refresh/`)."""

    permission_classes = [AllowAny]
    serializer_class = RefreshTokenSerializer

    @extend_schema(
        request=RefreshTokenSerializer,
        summary="Rotate JWT token pair.",
        description="Receives a valid refresh token and returns a new access token and rotated refresh token.",
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = AuthService()
        tokens = auth_service.refresh_tokens(
            refresh_token_str=serializer.validated_data["refresh"]
        )

        return success_response(data=tokens, message="Token refreshed successfully.")


class VerifyTokenAPIView(APIView):
    """Endpoint for token validation (`POST /api/v1/auth/verify/`)."""

    permission_classes = [AllowAny]

    @extend_schema(
        summary="Verify token validity.",
        description="Checks whether a given JWT token string is structurally valid and unexpired.",
    )
    def post(self, request: Request) -> Response:
        token_str = request.data.get("token")
        auth_service = AuthService()
        is_valid = auth_service.verify_token(token_str)
        return success_response(
            data={"valid": is_valid},
            message="Token verification completed.",
        )


class CurrentUserAPIView(APIView):
    """Endpoint for fetching current authenticated profile (`GET /api/v1/auth/me/`)."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Retrieve current user profile.",
        description="Returns full profile details of the authenticated user sending the request.",
    )
    def get(self, request: Request) -> Response:
        serializer = UserSerializer(request.user)
        return success_response(
            data=serializer.data, message="Profile retrieved successfully."
        )


class ProfileUpdateAPIView(APIView):
    """Endpoint for updating current user profile (`PUT/PATCH /api/v1/auth/profile/`)."""

    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    @extend_schema(
        request=UserUpdateSerializer,
        summary="Update current user profile.",
        description="Updates profile attributes such as full name, phone number, email, or username.",
    )
    def put(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_service = UserService()
        updated_user = user_service.update_user_profile(
            user_id=request.user.id, **serializer.validated_data
        )
        return success_response(
            data=UserSerializer(updated_user).data,
            message="Profile updated successfully.",
        )

    @extend_schema(
        request=UserUpdateSerializer,
        summary="Partially update current user profile.",
        description="Partially updates profile attributes.",
    )
    def patch(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        user_service = UserService()
        updated_user = user_service.update_user_profile(
            user_id=request.user.id, **serializer.validated_data
        )
        return success_response(
            data=UserSerializer(updated_user).data,
            message="Profile updated successfully.",
        )


class ChangePasswordAPIView(APIView):
    """Endpoint for changing password (`POST /api/v1/auth/change-password/`)."""

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    @extend_schema(
        request=ChangePasswordSerializer,
        summary="Change user password.",
        description="Validates current password and sets a new strong password.",
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = AuthService()
        auth_service.change_password(
            user=request.user,
            old_password=serializer.validated_data["old_password"],
            new_password=serializer.validated_data["new_password"],
        )
        return success_response(data={}, message="Password changed successfully.")


class ForgotPasswordAPIView(APIView):
    """Endpoint for initiating password reset (`POST /api/v1/auth/forgot-password/`)."""

    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    @extend_schema(
        request=ForgotPasswordSerializer,
        summary="Request password reset link.",
        description="Dispatches recovery instructions if account exists.",
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = AuthService()
        result = auth_service.forgot_password(email=serializer.validated_data["email"])
        return success_response(data=result, message=result["message"])


class ResetPasswordAPIView(APIView):
    """Endpoint for completing password reset (`POST /api/v1/auth/reset-password/`)."""

    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    @extend_schema(
        request=ResetPasswordSerializer,
        summary="Complete password reset with token.",
        description="Applies new password if verification token is valid.",
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = AuthService()
        auth_service.reset_password(
            token=serializer.validated_data["token"],
            new_password=serializer.validated_data["new_password"],
        )
        return success_response(data={}, message="Password reset successfully.")


class VerifyEmailAPIView(APIView):
    """Endpoint for verifying account email (`POST /api/v1/auth/verify-email/`)."""

    permission_classes = [AllowAny]
    serializer_class = VerifyEmailSerializer

    @extend_schema(
        request=VerifyEmailSerializer,
        summary="Verify email address with token.",
        description="Marks user email identity as verified.",
    )
    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        auth_service = AuthService()
        user = auth_service.verify_email(token=serializer.validated_data["token"])
        return success_response(
            data={"user": UserSerializer(user).data},
            message="Email address verified successfully.",
        )
