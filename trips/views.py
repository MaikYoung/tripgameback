from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from notifications.models import Notification
from points.models import Point
from trips.models import Trip
from trips.serializers import TripSerializer, TripDetailSerializer, CreateTripSerializer
from users.models import User


class TripListPaginated(ListAPIView):
    queryset = Trip.objects.all().order_by('create_at')
    serializer_class = TripSerializer
    pagination_class = PageNumberPagination


class TripCreate(APIView):
    def post(self, request):
        user = get_object_or_404(User.objects.all(), id=request.user.id)
        if user and user.id == request.data.get('owner', None):
            trip = Trip.create_trip(obj=request.data, user=user)
            if isinstance(trip, str):
                return JsonResponse(trip, status=status.HTTP_400_BAD_REQUEST, safe=False)
            else:
                trip_points_calculated = Point.calculate_points_by_trip_kms(trip.kms)
                trip.points = trip.points + trip_points_calculated
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

    def put(self, request, pk):
        trip = get_object_or_404(queryset=self.queryset, id=pk)
        serializer = CreateTripSerializer(instance=trip, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            returned_serializer = TripDetailSerializer(serializer.instance)
            return JsonResponse(returned_serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            #TODO: resolver la devolucion de errores!
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)


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
                trip_mate.points = trip_mate.points + (trip.points / 2)
                Notification.create_notification(
                    to_user=trip_mate, from_user=trip_owner.id, type='6', trip_related=trip.id
                )
                serializer = TripDetailSerializer(trip)
                return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            response = 'Not Authorized'
            return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED, safe=False)


class DeleteTripMate(APIView):
    queryset = User.objects.all()

    def post(self, request, pk, user):
        trip_owner = get_object_or_404(queryset=self.queryset, id=request.user.id)
        trip_mate = get_object_or_404(queryset=self.queryset, id=user)
        trip = get_object_or_404(Trip.objects.all(), id=pk)
        if trip_owner.id == trip.owner.id:
            if trip_mate.id in trip.mates:
                trip.mates.remove(trip_mate.id)
                trip_mate.points = trip_mate.points - (trip.points / 2)
                trip.save()
                serializer = TripDetailSerializer(trip)
                return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
            else:
                response = 'User is not a trip mate'
                return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            response = 'Not Authorized'
            return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED, safe=False)


class UploadPictureTrip(APIView):
    queryset = Trip.objects.all()

    def post(self, request, pk):
        trip = get_object_or_404(self.queryset, id=pk)
        owner = get_object_or_404(User.objects.all(), id=request.user.id)
        if owner.id == trip.owner.id:
            if len(trip.pictures) > 4:  # es una cuenta con 0 el primero
                response = '5 pictures is the limit'
                return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST, safe=False)
            else:
                image = request.data.get('image', None)
                if image is not None:
                    trip.pictures.append(image)
                    trip.points = trip.points + 5
                    trip.save()
                    returned_trip = get_object_or_404(self.queryset, id=trip.id)
                    serializer = TripDetailSerializer(returned_trip)
                    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
                else:
                    response = 'Image is None'
                    return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            response = 'Not Authorized'
            return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED, safe=False)


class DeletePictureTrip(APIView):
    queryset = Trip.objects.all()

    def delete(self, request, pk, index):
        trip = get_object_or_404(self.queryset, id=pk)
        owner = get_object_or_404(User.objects.all(), id=request.user.id)
        if owner.id == trip.owner.id:
            if len(trip.pictures) == 0:
                response = 'No pictures to delete'
                return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST, safe=False)
            else:
                for i, data in enumerate(trip.pictures):
                    if index == i:
                        trip.pictures.remove(data)
                        trip.points = trip.points - 5
                        trip.save()
                        returned_trip = get_object_or_404(self.queryset, id=trip.id)
                        serializer = TripDetailSerializer(returned_trip)
                        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            response = 'Not Authorized'
            return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED, safe=False)


class VerifyTrip(APIView):
    queryset = Trip.objects.all()

    def post(self, request, pk):
        trip = get_object_or_404(self.queryset, id=pk)
        user = get_object_or_404(User.objects.all(), id=request.user.id)
        if trip.owner.id == user.id:
            response = 'Can\'t verify your own trip'
            return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED, safe=False)
        elif user.id in trip.mates:
            response = 'Can\'t verify a trip if you are a mate'
            return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED, safe=False)
        else:
            if user.id in trip.verified_by:
                response = 'Can\'t verify a trip twice'
                return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED, safe=False)
            else:
                if len(trip.verified_by) < 2:
                    trip.verified_by.append(user.id)
                    trip.verified = True if len(trip.verified_by) == 2 else False
                    user.points = user.points + 5
                    user.save()
                    trip.save()
                    Notification.create_notification(
                        to_user=trip.owner, from_user=user.id, type='3', trip_related=trip.id
                    )
                    returned_trip = get_object_or_404(self.queryset, id=trip.id)
                    if returned_trip.verified:
                        Notification.create_notification(
                            to_user=trip.owner, from_user=0, type='4', trip_related=trip.id
                        )
                    serializer = TripDetailSerializer(returned_trip)
                    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
                else:
                    response = 'Trip is already verified'
                    return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST, safe=False)
