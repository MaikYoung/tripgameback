from rest_framework import serializers

from medals.models import Medals


class MedalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medals
        fields = '__all__'