"""Django AppConfig for Notifications Module."""

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "modules.notifications"

    def ready(self):
        import modules.notifications.signals

    verbose_name = "Notifications Module"
