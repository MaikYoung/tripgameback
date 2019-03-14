from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from points.models import Point
from points.serializers import PointDetailSerializer
from trips.models import Trip


class PointsUserDetail(APIView):
    def get(self, request):
        point = get_object_or_404(Point.objects.all(), owner=request.user.id)
        trips = Trip.objects.filter(owner=request.user.id)
        list_kms = []
        for trip in trips:
            if trip.verified is True:
                list_kms.append(trip.kms)
        total_kms = sum(list_kms)
        if total_kms != point.total_kms:
            point.total_kms = total_kms
            point.save()
            serializer = PointDetailSerializer(point)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            serializer = PointDetailSerializer(point)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)