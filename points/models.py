from django.db import models
from rest_framework.generics import get_object_or_404

from users.models import User


class Point(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    total_kms = models.IntegerField(default=0)

    @staticmethod
    def create_point_by_user(owner):
        point = Point()
        point.owner = owner
        point.save()
        return point

    @staticmethod
    def sum_points_for_user_by_trip(user_id, num):
        point = get_object_or_404(Point.objects.all(), owner=user_id)
        point.points = point.points + num
        point.save()
        return point

    @staticmethod
    def calculate_points_by_trip_kms(kms):
        if kms <= 500:
            return 25
        elif (kms >= 501) or (kms <= 1000):
            return 50
        elif (kms >= 1001) or (kms <= 2000):
            return 100
        elif (kms >= 2001) or (kms <= 5000):
            return 200
        elif (kms >= 5001) or (kms <= 10000):
            return 500
        elif kms >= 10001:
            return 1000
