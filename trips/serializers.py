import datetime

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from project.settings import LEVELS, geolocator
from trips.models import Trip
from users.models import User


class TripSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ('id', 'pictures', 'kms', 'user')

    @staticmethod
    def get_user(obj):
        user = get_object_or_404(User.objects.all(), id=obj.owner.id)
        return {'id': user.pk, 'username': user.username, 'trip_level': LEVELS[int(user.trip_level)][1]}


class TripDetailSerializer(serializers.ModelSerializer):
    trip_mates = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = (
            'id', 'owner', 'from_to', 'destiny', 'pictures', 'verified', 'kms', 'route', 'trip_mates', 'views',
            'counter_verified',
        )

    @staticmethod
    def get_trip_mates(obj):
        trip_mates = []
        if len(obj.mates) > 0:
            for mate in obj.mates:
                user = get_object_or_404(User.objects.all(), id=mate)
                trip_mates.append(
                    {'user_id': user.id, 'username': user.username, 'trip_level': LEVELS[int(user.trip_level)][1]}
                )
            return trip_mates
        return trip_mates

    @staticmethod
    def get_owner(obj):
        owner = get_object_or_404(User.objects.all(), id=obj.owner.id)
        return {'id': owner.id, 'username': owner.username, 'trip_level': LEVELS[int(owner.trip_level)][1]}


class CreateTripSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    owner = serializers.IntegerField(required=True)
    destiny = serializers.CharField(required=True)
    from_to = serializers.CharField(required=True)
    verified = serializers.BooleanField(required=False)
    counter_verified = serializers.IntegerField(required=False)
    route = serializers.CharField(required=True)
    kms = serializers.IntegerField(required=False)
    views = serializers.IntegerField(required=False)
    date_start = serializers.DateField(required=True)
    date_end = serializers.DateField(required=True)

    def update(self, instance, validated_data):
        pass


