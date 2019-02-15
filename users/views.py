from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer


class ListUsers(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)


class DetailUser(APIView):
    def get(self, request, pk):
        user = User.objects.filter(id=pk)
        if user:
            serializer = UserDetailSerializer(user, many=True)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            response = 'User does not exit'
            return JsonResponse(response, status=status.HTTP_404_NOT_FOUND, safe=False)
