from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from medals.models import Medals
from medals.serializers import MedalSerializer
from trips.models import Trip
from users.models import User


class ListMedals(APIView):

    def get(self, request):
        user = get_object_or_404(User.objects.all(), id=request.user.id)
        medals = get_object_or_404(Medals.objects.all(), owner=request.user.id)
        trips = Trip.objects.filter(owner=user)
        for trip in trips:
            if trip.trip_type == '0':
                if medals.ski is False:
                    medals.ski_count = medals.ski_count + 1
                    if medals.ski_count == 6:
                        medals.ski = True
            elif trip.trip_type == '1':
                if medals.trekking is False:
                    medals.trekking_count = medals.trekking_count + 1
                    if medals.trekking_count == 6:
                        medals.trekking = True
            elif trip.trip_type == '2':
                if medals.cultural is False:
                    medals.cultural_count = medals.cultural_count + 1
                    if medals.cultural_count == 6:
                        medals.cultural = True
            elif trip.trip_type == '3':
                if medals.beach is False:
                    medals.beach_count = medals.beach_count + 1
                    if medals.beach_count == 6:
                        medals.beach = True
            elif trip.trip_type == '4':
                if medals.party is False:
                    medals.party_count = medals.party_count + 1
                    if medals.party_count == 6:
                        medals.party = True
            elif trip.trip_type == '5':
                if medals.festival is False:
                    medals.festival_count = medals.festival_count + 1
                    if medals.festival_count == 6:
                        medals.festival = True
            elif trip.trip_type == '6':
                if medals.surf is False:
                    medals.surf_count = medals.surf_count + 1
                    if medals.surf_count == 6:
                        medals.surf = True
            elif trip.trip_type == '8':
                if medals.gastronomic is False:
                    medals.gastronomic_count = medals.gastronomic_count + 1
                    if medals.gastronomic_count == 6:
                        medals.gastronomic = True
            medals.save()
        serializer = MedalSerializer(medals)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
