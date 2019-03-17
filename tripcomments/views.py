from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from tripcomments.models import TripComments
from tripcomments.serializers import ListCommentByTripSerializer
from trips.models import Trip
from users.models import User


class ListComments(APIView):

    def get(self, request, trip):
        comments = TripComments.objects.filter(trip=trip)
        if comments:
            serializer = ListCommentByTripSerializer(comments, many=True)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse([], status=status.HTTP_204_NO_CONTENT, safe=False)


class CreateUpdateComment(APIView):

    def post(self, request, pk):
        user = get_object_or_404(User.objects.all(), id=request.user.id)
        comment = request.data.get('comment', None)
        trip = get_object_or_404(Trip.objects.all(), id=pk)
        result = TripComments.create_comment_by_trip(
            user=user, trip=trip, text=comment
        )
        if result:
            comments = TripComments.objects.filter(trip=pk)
            if comments:
                serializer = ListCommentByTripSerializer(comments, many=True)
                return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse([], status=status.HTTP_400_BAD_REQUEST, safe=False)

    def put(self, request, trip, pk):
        owner = get_object_or_404(User.objects.all(), id=request.user.id)
        comment = get_object_or_404(TripComments.objects.all(), id=pk)
        if owner.id == comment.publisher.id:
            comment_updated = TripComments.update_comment(
                comment=request.data.get('comment', None), id=pk
            )
            if comment_updated:
                comments = TripComments.objects.filter(trip=trip)
                if comments:
                    serializer = ListCommentByTripSerializer(comments, many=True)
                    return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            response = 'Not Authorized'
            return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED, safe=False)

    def delete(self, request, trip, pk):
        owner = get_object_or_404(User.objects.all(), id=request.user.id)
        comment = get_object_or_404(TripComments.objects.all(), id=pk)
        if owner.id == comment.publisher.id:
            comment_deleted = get_object_or_404(TripComments.objects.all(), id=pk)
            comment_deleted.delete()
            response = True
            return JsonResponse(response, status=status.HTTP_200_OK, safe=False)
        else:
            response = 'Not Authorized'
            return JsonResponse(response, status=status.HTTP_401_UNAUTHORIZED, safe=False)
