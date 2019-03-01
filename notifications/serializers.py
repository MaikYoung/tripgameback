from rest_framework import serializers

from notifications.models import Notification
from project.settings import NOTIFICATION_TYPES


class NotificationSerializer(serializers.ModelSerializer):
    trip_type = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('from_user', 'to_user', 'trip_type', 'trip_related')

    def get_trip_type(self, obj):
        return NOTIFICATION_TYPES[int(obj.type)][1]
