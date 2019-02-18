from django.contrib.auth.models import AbstractUser
from django.db import models
from project.settings import LEVELS


class User(AbstractUser):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, null=True, unique=True)
    password = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    trip_level = models.CharField(max_length=2, choices=LEVELS, default=0)
    based_on = models.CharField(max_length=50, blank=True, null=True)
    profile_pic = models.URLField(blank=True, null=True)


