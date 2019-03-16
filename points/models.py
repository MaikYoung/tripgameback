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
        if kms > 50:
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
        else:
            return 0

    @staticmethod
    def calculate_user_trip_level_by_user_points(points):
        if points <= 40:
            return 0  #new
        elif (points >= 41) or (points <= 400):
            return 1  #noob
        elif (points >= 401) or (points <= 1000):
            return 2  #begginer
        elif (points >= 1001) or (points <= 1800):
            return 3  #junior
        elif (points >= 1801) or (points <= 3000):
            return 4  #sophomore
        elif (points >= 3001) or (points <= 5000):
            return 5  #intermediate
        elif (points >= 5001) or (points <= 10000):
            return 6  #backpacker
        elif (points >= 10001) or (points <= 16000):
            return 7  #advanced
        elif (points >= 16001) or (points <= 25000):
            return 8  #high authority
        elif (points >= 25001) or (points <= 40000):
            return 9  #master
        elif points >= 40001:
            return 10  #true traveler

