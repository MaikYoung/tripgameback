from django.contrib.postgres.fields import JSONField
from django.db import models

from project.settings import NOTIFICATION_TYPES
from users.models import User


class Notification(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    from_user = models.IntegerField()
    type = models.CharField(choices=NOTIFICATION_TYPES, max_length=1)
    extra_info = JSONField()
    active = models.BooleanField(default=True)
    create_date = models.DateField(auto_now_add=True)

    def create_notification(self, from_user, to_user, type, extra_info):
        notification = {
            'from_user': from_user,
            'to_user': to_user,
            'type': type
        }
        notification = Notification.objects.create(notification)
        if extra_info:
            notification.update(extra_info=extra_info)

    def set_inactive_notification(self, pk, active):
        notification = Notification.objects.filter(id=pk)
        notification.update(active=active)

    def delete_notification_after_30_days(self):
        pass


