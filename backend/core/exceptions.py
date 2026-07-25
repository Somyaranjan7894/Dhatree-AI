"""
Custom API exceptions and standardized exception handler for Dhatree AI.
Ensures every error returned by the API follows a consistent JSON schema.
"""

from typing import Any, Dict, Optional

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


class BaseDhatreeException(APIException):
    """Base exception class for all Dhatree AI domain errors."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "An internal platform error occurred."
    default_code = "dhatree_internal_error"


class BusinessRuleViolationError(BaseDhatreeException):
    """Raised when a business constraint or invariant is breached."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "A business rule violation occurred."
    default_code = "business_rule_violation"


class ResourceNotFoundError(BaseDhatreeException):
    """Raised when a requested domain entity does not exist."""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "The requested resource was not found."
    default_code = "resource_not_found"


class ModelInferenceError(BaseDhatreeException):
    """Raised when an AI engine prediction or vision analysis fails."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "AI model inference service is temporarily unavailable."
    default_code = "ai_inference_error"


from rest_framework.exceptions import AuthenticationFailed as DRFAuthenticationFailed
from rest_framework.exceptions import PermissionDenied as DRFPermissionDenied
from rest_framework.exceptions import ValidationError as DRFValidationError


class AuthenticationFailed(DRFAuthenticationFailed):
    """Raised when authentication credentials or token validation fails."""

    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Authentication failed."
    default_code = "authentication_failed"


class PermissionDenied(DRFPermissionDenied):
    """Raised when an authenticated user lacks required role or ownership permissions."""

    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You do not have permission to perform this action."
    default_code = "permission_denied"


class ValidationError(DRFValidationError):
    """Raised when input data fails schema or business validation rules."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid input data."
    default_code = "validation_error"


import logging

logger = logging.getLogger("dhatree.error")


def custom_exception_handler(
    exc: Exception, context: Dict[str, Any]
) -> Optional[Response]:
    """
    Standardized DRF exception handler.
    Formats all error payloads into:
    {
        "success": false,
        "message": "Human readable summary",
        "errors": { ... validation errors or field details ... }
    }
    Never exposes internal exceptions or tracebacks.
    """
    response = exception_handler(exc, context)

    if response is not None:
        error_code = getattr(exc, "default_code", "api_error")
        error_message = (
            str(exc.detail)
            if hasattr(exc, "detail")
            and isinstance(exc.detail, (str, getattr(exc, "detail").__class__))
            and not isinstance(exc.detail, (dict, list))
            else "A validation or processing error occurred."
        )
        if hasattr(exc, "detail") and isinstance(exc.detail, str):
            error_message = exc.detail
        elif (
            hasattr(exc, "detail")
            and isinstance(exc.detail, list)
            and exc.detail
            and isinstance(exc.detail[0], str)
        ):
            error_message = exc.detail[0]
        elif str(exc) and not isinstance(getattr(exc, "detail", None), (dict, list)):
            error_message = str(exc)

        errors = (
            response.data
            if isinstance(response.data, (dict, list))
            else {"detail": response.data}
        )

        # Clean up response payload structure
        response.data = {
            "success": False,
            "message": error_message,
            "errors": errors,
            "code": error_code,
        }
    else:
        # Log unexpected internal exceptions without exposing tracebacks to client
        logger.exception(
            f"Unhandled internal exception in {context.get('view')}: {exc}",
            exc_info=exc,
        )
        response = Response(
            {
                "success": False,
                "message": "An internal platform error occurred.",
                "errors": {"detail": "Internal server error."},
                "code": "internal_error",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response
