from rest_framework import serializers

from points.models import Point


class PointDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ('owner', 'points', 'total_kms')
