from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from tripcomments.models import TripComments
from tripcomments.serializers import ListTripSerializer


class ListComments(APIView):

    def get(self, request, pk):
        comments = TripComments.objects.filter(trip=pk)
        if comments:
            serializer = ListTripSerializer(comments, many=True)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse([], status=status.HTTP_204_NO_CONTENT, safe=False)

