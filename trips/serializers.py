

from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from project.settings import LEVELS, TRIP_TYPES
from trips.models import Trip
from trips.validators import validate_date_start, validate_date_end, validate_from_to
from users.models import User


class TripSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ('id', 'pictures', 'kms', 'user', 'verified', 'likes')

    @staticmethod
    def get_user(obj):
        user = get_object_or_404(User.objects.all(), id=obj.owner.id)
        return {'id': user.pk, 'username': user.username, 'trip_level': LEVELS[int(user.trip_level)][1]}

    @staticmethod
    def get_likes(obj):
        return len(obj.likes)


class TripSerializerPaginated(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = ('id', 'pictures', 'kms', 'user', 'verified', 'likes')

    @staticmethod
    def get_user(obj):
        owner = obj.get('owner', None)
        user = get_object_or_404(User.objects.all(), id=owner.id)
        return {'id': user.pk, 'username': user.username, 'trip_level': LEVELS[int(user.trip_level)][1]}

    @staticmethod
    def get_likes(obj):
        likes = obj.get('likes', None)
        return len(likes)


class TripDetailSerializer(serializers.ModelSerializer):
    trip_mates = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    pictures = serializers.SerializerMethodField()
    verified_by = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = (
            'id', 'owner', 'from_to', 'destiny', 'date_start', 'date_end', 'pictures', 'verified', 'kms', 'route',
            'trip_mates', 'views', 'verified_by', 'likes', 'type'
        )

    @staticmethod
    def get_likes(obj):
        return len(obj.likes)

    @staticmethod
    def get_type(obj):
        return TRIP_TYPES[int(obj.trip_type)][1]

    @staticmethod
    def get_trip_mates(obj):
        trip_mates = []
        if len(obj.mates) > 0:
            for mate in obj.mates:
                user = get_object_or_404(User.objects.all(), id=mate)
                trip_mates.append(
                    {'id': user.id, 'username': user.username, 'trip_level': LEVELS[int(user.trip_level)][1]}
                )
            return trip_mates
        return trip_mates

    @staticmethod
    def get_verified_by(obj):
        verified_by = []
        if len(obj.verified_by) > 0:
            for usr in obj.verified_by:
                user = get_object_or_404(User.objects.all(), id=usr)
                verified_by.append(
                    {'id': user.id, 'username': user.username, 'trip_level': LEVELS[int(user.trip_level)][1]}
                )
            return verified_by
        return verified_by

    @staticmethod
    def get_owner(obj):
        owner = get_object_or_404(User.objects.all(), id=obj.owner.id)
        return {'id': owner.id, 'username': owner.username, 'trip_level': LEVELS[int(owner.trip_level)][1]}

    @staticmethod
    def get_pictures(obj):
        pictures = []
        for i, data in enumerate(obj.pictures):
            obj = {'index': i, 'image': data}
            pictures.append(obj)
        return pictures


class CreateTripSerializer(serializers.Serializer):
    destiny = serializers.CharField(required=True)
    from_to = serializers.CharField(required=True)
    route = serializers.CharField(required=True)
    date_start = serializers.DateField(required=True)
    date_end = serializers.DateField(required=True)

    def update(self, instance, validated_data):
        request_date_start = validated_data.get('date_start', None)
        if request_date_start is not None:
            validate = validate_date_start(str(request_date_start))
            if validate == 'error':
                return 'Can\'t publish trips older than 2 years'
            instance.date_start = validated_data.get('date_start', instance.date_start)
        request_date_end = validated_data.get('date_end', None)
        if request_date_end is not None:
            validate = validate_date_end(date_start=str(instance.date_start), date_end=str(request_date_end))
            if validate == 'error':
                return 'Date start can\'t be greater that Date end'
            instance.date_end = validated_data.get('date_end', instance.date_end)
        request_from_to = validated_data.get('from_to', None)
        if request_from_to is not None:
            validate = validate_from_to(request_from_to)
            if validate == 'error':
                return 'City from_to can\'t be found'
            instance.from_to = validated_data.get('from_to', instance.from_to)
        request_destiny = validated_data.get('destiny', None)
        if request_from_to is not None:
            validate = validate_from_to(request_destiny)
            if validate == 'error':
                return 'City destiny can\'t be found'
            instance.destiny = validated_data.get('destiny', instance.destiny)
        instance.route = validated_data.get('route', instance.route)
        instance.save()
        return instance

