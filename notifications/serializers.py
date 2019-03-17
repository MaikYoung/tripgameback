from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from notifications.models import Notification
from project.settings import NOTIFICATION_TYPES
from trips.models import Trip
from users.models import User


class NotificationSerializer(serializers.ModelSerializer):
    trip_type = serializers.SerializerMethodField()
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()
    trip_related = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'from_user', 'to_user', 'trip_type', 'trip_related')

    @staticmethod
    def get_trip_type(obj):
        return NOTIFICATION_TYPES[int(obj.type)][1]

    @staticmethod
    def get_from_user(obj):
        if obj.from_user != 0:
            from_user = get_object_or_404(User.objects.all(), id=obj.from_user)
            return {'id': from_user.id, 'username': from_user.username}
        else:
            return 0

    @staticmethod
    def get_to_user(obj):
        to_user = get_object_or_404(User.objects.all(), id=obj.to_user.id)
        return {'id': to_user.id, 'username': to_user.username}

    @staticmethod
    def get_trip_related(obj):
        if obj.trip_related is None:
            return []
        else:
            trip = get_object_or_404(Trip.objects.all(), id=obj.trip_related)
            return {'id': trip.id, 'destiny': trip.destiny}
