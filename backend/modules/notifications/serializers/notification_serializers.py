from rest_framework import serializers

from modules.notifications.models.notification import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "title",
            "description",
            "notification_type",
            "category",
            "is_read",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
