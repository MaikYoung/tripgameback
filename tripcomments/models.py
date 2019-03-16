from django.db import models

from trips.models import Trip
from users.models import User


class TripComments(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
