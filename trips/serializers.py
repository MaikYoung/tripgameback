from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from project.settings import LEVELS
from trips.models import Trip
from users.models import User


class TripSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ('id', 'pictures', 'kms', 'user')

    def get_user(self, obj):
        user = get_object_or_404(User.objects.all(), id=obj.owner.id)
        return {'id': user.pk, 'username': user.username, 'trip_level': LEVELS[int(user.trip_level)][1]}


class TripDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
