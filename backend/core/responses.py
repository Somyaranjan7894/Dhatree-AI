"""
Standardized API Response formatters for Dhatree AI.
Enforces uniform JSON payload schema across all REST endpoints:
Success Example:
{
    "success": true,
    "message": "Operation completed successfully.",
    "data": { ... }
}
Error Example:
{
    "success": false,
    "message": "Validation error.",
    "errors": { ... }
}
"""
from typing import Any, Optional
from rest_framework import status
from rest_framework.response import Response


def success_response(
    data: Any = None,
    message: str = "Operation completed successfully.",
    status_code: int = status.HTTP_200_OK,
) -> Response:
    """
    Returns a standardized successful JSON Response.
    """
    payload = {
        "success": True,
        "message": message,
        "data": data if data is not None else {},
    }
    return Response(payload, status=status_code)


def error_response(
    errors: Any = None,
    message: str = "An error occurred during operation execution.",
    status_code: int = status.HTTP_400_BAD_REQUEST,
    code: Optional[str] = None,
) -> Response:
    """
    Returns a standardized error JSON Response.
    """
    payload = {
        "success": False,
        "message": message,
        "errors": errors if errors is not None else {},
    }
    if code:
        payload["code"] = code
    return Response(payload, status=status_code)


def paginated_response(
    paginator: Any,
    data: Any,
    message: str = "Retrieved paginated records successfully.",
    status_code: int = status.HTTP_200_OK,
) -> Response:
    """
    Returns a standardized paginated successful JSON Response matching the project schema.
    """
    count = (
        paginator.page.paginator.count
        if hasattr(paginator, "page") and hasattr(paginator.page, "paginator")
        else (len(data) if isinstance(data, list) else 0)
    )
    paginated_data = {
        "count": count,
        "next": paginator.get_next_link() if hasattr(paginator, "get_next_link") else None,
        "previous": paginator.get_previous_link() if hasattr(paginator, "get_previous_link") else None,
        "results": data,
    }
    return success_response(data=paginated_data, message=message, status_code=status_code)

