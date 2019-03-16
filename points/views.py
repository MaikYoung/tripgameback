from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from points.models import Point
from points.serializers import PointDetailSerializer
from trips.models import Trip
from users.models import User


class PointsUserDetail(APIView):
    def get(self, request):
        point = get_object_or_404(Point.objects.all(), owner=request.user.id)
        user = get_object_or_404(User.objects.all(), id=request.user.id)
        trips = Trip.objects.filter(owner=request.user.id)
        list_kms = []
        list_points = []
        for trip in trips:
            if trip.verified is True:
                list_kms.append(trip.kms)
                list_points.append(trip.points)
        total_kms = sum(list_kms)
        if total_kms != point.total_kms:
            point.total_kms = total_kms
        total_points = sum(list_points)
        if total_points != point.points:
            point.points = total_points
        point.points = point.points + user.points
        point.save()
        serializer = PointDetailSerializer(point)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)