from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationList(APIView):

    def get(self, request):
        notification = Notification.objects.filter(to_user=request.user.id, active=True)
        serializer = NotificationSerializer(notification, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)