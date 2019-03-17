from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from tripcomments.models import TripComments
from users.models import User


class ListCommentByTripSerializer(serializers.ModelSerializer):
    publisher = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = TripComments
        fields = ('id', 'comment', 'publisher', 'created_at')

    @staticmethod
    def get_publisher(obj):
        publisher = get_object_or_404(User.objects.all(), id=obj.publisher.id)
        return {'id': publisher.id, 'username': publisher.username}

    @staticmethod
    def get_created_at(obj):
        return obj.created_at.strftime('%d-%m-%Y %H:%M:%S')
