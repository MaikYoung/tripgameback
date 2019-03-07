from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from trips.models import Trip
from trips.serializers import TripSerializer, TripDetailSerializer


class TripList(APIView):
    def get(self, request):
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


class TripDetail(APIView):
    queryset = Trip.objects.all()

    def get(self, request, pk):
        trip = get_object_or_404(queryset=self.queryset, id=pk)
        serializer = TripDetailSerializer(trip)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
