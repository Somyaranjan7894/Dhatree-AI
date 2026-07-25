"""
Custom User Model definition for Dhatree AI Digital Agriculture Platform.
Uses UUID primary keys, email uniqueness, role-based access control, and soft deletion.
"""
import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom manager for User model supporting email/username login, role assignment,
    and excluding soft-deleted accounts by default when using `active_objects`.
    """

    def create_user(
        self, email: str, username: str, password: str = None, **extra_fields
    ):
        if not email:
            raise ValueError(_("An email address must be provided."))
        if not username:
            raise ValueError(_("A unique username must be provided."))

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_deleted", False)

        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, username: str, password: str = None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", User.Role.ADMIN)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, username, password, **extra_fields)


class ActiveUserManager(models.Manager):
    """Manager returning only non-deleted (`is_deleted=False`) active user instances."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class User(AbstractUser):
    """
    Enterprise user profile model for Dhatree AI.
    Subclasses AbstractUser to replace integer IDs with UUID v4 and add domain fields.
    """

    class Role(models.TextChoices):
        FARMER = "farmer", _("Farmer")
        ADMIN = "admin", _("Platform Administrator")
        OFFICER = "officer", _("Agriculture Extension Officer")
        RESEARCHER = "researcher", _("Agricultural Scientist / Researcher")
        STUDENT = "student", _("Student / Academic")

    class AccountStatus(models.TextChoices):
        ACTIVE = "active", _("Active")
        SUSPENDED = "suspended", _("Suspended")
        DEACTIVATED = "deactivated", _("Deactivated")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Unique UUID v4 primary key for this user profile."),
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        db_index=True,
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        db_index=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    full_name = models.CharField(
        _("full name"),
        max_length=255,
        blank=True,
    )
    phone_number = models.CharField(
        _("phone number"),
        max_length=20,
        blank=True,
        null=True,
    )
    profile_photo = models.ImageField(
        _("profile photo"),
        upload_to="profiles/%Y/%m/",
        blank=True,
        null=True,
    )
    role = models.CharField(
        _("user role"),
        max_length=30,
        choices=Role.choices,
        default=Role.FARMER,
        db_index=True,
    )
    account_status = models.CharField(
        _("account status"),
        max_length=30,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
        db_index=True,
    )
    is_verified = models.BooleanField(
        _("verified identity"),
        default=False,
        help_text=_("Designates whether this user has verified their email/phone."),
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("updated at"),
        auto_now=True,
    )
    is_deleted = models.BooleanField(
        _("soft deleted"),
        default=False,
        db_index=True,
    )
    deleted_at = models.DateTimeField(
        _("deleted at"),
        blank=True,
        null=True,
    )

    objects = UserManager()
    active_objects = ActiveUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.email} ({self.get_role_display()})"

    def soft_delete(self) -> None:
        """Marks the user profile as deleted without scrubbing audit history."""
        self.is_deleted = True
        self.is_active = False
        self.account_status = self.AccountStatus.DEACTIVATED
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "is_active", "account_status", "deleted_at", "updated_at"])
