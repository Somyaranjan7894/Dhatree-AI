"""
Notification model definition.
Represents an alert or informational message sent to a user.
"""
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

class ActiveNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Notification(models.Model):
    """
    System notification dispatched to a user.
    """
    class NotificationType(models.TextChoices):
        INFORMATION = "information", _("Information")
        SUCCESS = "success", _("Success")
        WARNING = "warning", _("Warning")
        CRITICAL = "critical", _("Critical")

    class NotificationCategory(models.TextChoices):
        PREDICTION = "prediction", _("Prediction")
        RECOMMENDATION = "recommendation", _("Recommendation")
        SYSTEM = "system", _("System")
        ALERT = "alert", _("Alert")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        help_text=_("User this notification is addressed to.")
    )
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"))
    notification_type = models.CharField(
        _("notification type"),
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.INFORMATION,
    )
    category = models.CharField(
        _("category"),
        max_length=20,
        choices=NotificationCategory.choices,
        default=NotificationCategory.SYSTEM,
    )
    is_read = models.BooleanField(_("read status"), default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False, db_index=True)

    objects = models.Manager()
    active_objects = ActiveNotificationManager()

    class Meta:
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.user.email}"

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=["is_read", "updated_at"])

    def soft_delete(self):
        self.is_deleted = True
        self.save(update_fields=["is_deleted", "updated_at"])
