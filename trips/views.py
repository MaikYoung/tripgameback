import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from trips.models import Trip
from trips.serializers import TripSerializer, TripDetailSerializer, CreateTripSerializer
from users.models import User


class TripList(APIView):
    def get(self, request):
        trips = Trip.objects.all().order_by()
        serializer = TripSerializer(trips, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    def post(self, request):
        user = get_object_or_404(User.objects.all(), id=request.user.id)
        if user and user.id == request.data.get('owner', None):
            trip = Trip.create_trip(obj=request.data, user=user)
            if isinstance(trip, str):
                return JsonResponse(trip, status=status.HTTP_400_BAD_REQUEST, safe=False)
            else:
                serializer = TripDetailSerializer(trip)
                return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        else:
            response = 'User request is not owner'
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST, safe=False)


class TripDetail(APIView):
    queryset = Trip.objects.all()

    def get(self, request, pk):
        trip = get_object_or_404(queryset=self.queryset, id=pk)
        serializer = TripDetailSerializer(trip)
        Trip.new_visit(trip=trip)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


class AddTripMate(APIView):
    queryset = User.objects.all()

    def post(self, request, pk, user):
        trip_owner = get_object_or_404(queryset=self.queryset, id=request.user.id)
        trip_mate = get_object_or_404(queryset=self.queryset, id=user)
        trip = get_object_or_404(Trip.objects.all(), id=pk)
        if trip_owner.id == trip.owner.id:
            if trip_mate.id in trip.mates:
                response = 'User is already a trip mate'
                return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST, safe=False)
            else:
                trip.mates.append(trip_mate.id)
                trip.save()
                serializer = TripDetailSerializer(trip)
                return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


class DeleteTripMate(APIView):
    pass

