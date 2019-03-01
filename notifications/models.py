from django.contrib.postgres.fields import JSONField
from django.db import models

from project.settings import NOTIFICATION_TYPES
from users.models import User


class Notification(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_user = models.IntegerField()
    type = models.CharField(choices=NOTIFICATION_TYPES, max_length=1)
    trip_related = models.IntegerField(default=None)
    active = models.BooleanField(default=True)
    create_date = models.DateField(auto_now_add=True)

    def create_notification(self, notice):
        pass



