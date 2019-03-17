from django.db import models
from rest_framework.generics import get_object_or_404

from trips.models import Trip
from users.models import User


class TripComments(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_comment_by_trip(trip, user, text):
        comment = TripComments()
        comment.trip = trip
        comment.publisher = user
        comment.comment = text
        comment.save()
        return True

    @staticmethod
    def update_comment(comment, id):
        comment_to_update = get_object_or_404(TripComments.objects.all(), id=id)
        comment_to_update.comment = comment
        comment_to_update.save()
        return comment_to_update
