from django.contrib.postgres.fields import JSONField
from django.db import models

from project.settings import NOTIFICATION_TYPES
from users.models import User


class Notification(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_user = models.IntegerField()
    type = models.CharField(choices=NOTIFICATION_TYPES, max_length=1)
    trip_related = models.IntegerField(default=None, null=True)
    active = models.BooleanField(default=True)
    create_date = models.DateField(auto_now_add=True)

    @staticmethod
    def create_notification(to_user, from_user, type, trip_related=None):
        notification = Notification()
        notification.to_user = to_user
        notification.from_user = from_user
        notification.type = type
        if trip_related:
            notification.trip_related = trip_related
        notification.save()




