"""
Reusable Role-Based Access Control (RBAC) permission classes for Dhatree AI.
Ensures every domain boundary can cleanly enforce role and ownership invariants.
"""
from typing import Any
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAuthenticated(BasePermission):
    """Allows access only to authenticated and active users."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and not getattr(request.user, "is_deleted", False)
        )


class IsAdmin(BasePermission):
    """Allows access only to platform administrators (`role == 'admin'` or `is_superuser`)."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not (request.user and request.user.is_authenticated):
            return False
        if getattr(request.user, "is_deleted", False):
            return False
        return bool(
            getattr(request.user, "role", "") == "admin"
            or request.user.is_superuser
            or request.user.is_staff
        )


class IsFarmer(BasePermission):
    """Allows access only to verified farmers (`role == 'farmer'`)."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        if not (request.user and request.user.is_authenticated):
            return False
        if getattr(request.user, "is_deleted", False):
            return False
        return bool(getattr(request.user, "role", "") == "farmer")


class OwnerOnly(BasePermission):
    """
    Object-level permission allowing modification or viewing only by the resource owner.
    Checks `obj == request.user`, `obj.user == request.user`, or `obj.owner == request.user`.
    """

    def has_object_permission(
        self, request: Request, view: APIView, obj: Any
    ) -> bool:
        if not (request.user and request.user.is_authenticated):
            return False
        if getattr(request.user, "is_deleted", False):
            return False
        # Platform admins can access or modify any object
        if getattr(request.user, "role", "") == "admin" or request.user.is_superuser:
            return True
        if obj == request.user:
            return True
        if hasattr(obj, "user") and obj.user == request.user:
            return True
        if hasattr(obj, "owner") and obj.owner == request.user:
            return True
        return False


class AdminOrReadOnly(BasePermission):
    """Allows read access to any authenticated user, but write permissions only to platform administrators."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return bool(request.user and request.user.is_authenticated)
        return bool(
            request.user
            and request.user.is_authenticated
            and (getattr(request.user, "role", "") == "admin" or request.user.is_superuser)
        )
