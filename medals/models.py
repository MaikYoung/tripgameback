from django.db import models
from rest_framework.generics import get_object_or_404

from users.models import User


class Medals(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    ski = models.BooleanField(default=False)
    ski_count = models.IntegerField(default=0)
    trekking = models.BooleanField(default=False)
    trekking_count = models.IntegerField(default=0)
    cultural = models.BooleanField(default=False)
    cultural_count = models.IntegerField(default=0)
    beach = models.BooleanField(default=False)
    beach_count = models.IntegerField(default=0)
    party = models.BooleanField(default=False)
    party_count = models.IntegerField(default=0)
    festival = models.BooleanField(default=False)
    festival_count = models.IntegerField(default=0)
    surf = models.BooleanField(default=False)
    surf_count = models.IntegerField(default=0)
    gastronomic = models.BooleanField(default=False)
    gastronomic_count = models.IntegerField(default=0)

    @staticmethod
    def create_medals(user):
        medals = Medals()
        medals.owner = user
        medals.save()
        return True

