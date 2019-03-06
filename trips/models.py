from django.contrib.postgres.fields import ArrayField
from django.db import models
from users.models import User


class Trip(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    mates = ArrayField(models.IntegerField(), default=list)
    destiny = models.CharField(max_length=100)
    from_to = models.CharField(max_length=100)
    pictures = ArrayField(models.URLField(blank=True, null=True), default=list, size=8)
    verified = models.BooleanField(default=False)
    kms = models.IntegerField()
    route = models.TextField(blank=True)
