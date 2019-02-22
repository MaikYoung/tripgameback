from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ('from_user', 'to_user', 'type', 'trip_related')


class CreateNotificationSerializer(serializers.ModelSerializer):
    to_user = serializers.PrimaryKeyRelatedField(read_only=True)
    from_user = serializers.IntegerField(read_only=True)
    type = serializers.IntegerField(read_only=True)
    trip_related = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        notification = Notification.objects.create(**validated_data)
        notification.save()
        return notification

