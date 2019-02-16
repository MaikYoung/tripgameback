from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer, UserCreateSerializer


class ListUsers(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe=False)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)


class DetailUser(APIView):
    queryset = User.objects.all()

    def get(self, request, pk):
        user = User.objects.filter(id=pk)
        if user:
            serializer = UserDetailSerializer(user, many=True)
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            response = 'User does not exit'
            return JsonResponse(response, status=status.HTTP_404_NOT_FOUND, safe=False)

    def put(self, request, pk):
        user = get_object_or_404(queryset=self.queryset, id=pk)
        serializer = UserCreateSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse({'id': serializer.data.get('id')},  status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    def delete(self, request, pk):
        # TODO: Mirar por que 'ConnectionResetError: [Errno 104] Connection reset by peer' despues de borrar un user
        if request.user.is_superuser:
            user = get_object_or_404(queryset=self.queryset, id=pk)
            user.delete()
            response = 'User deleted correctly'
            return JsonResponse(response, status=status.HTTP_204_NO_CONTENT, safe=False)
        else:
            response = 'Not Authorized'
            return JsonResponse(response, status=status.HTTP_403_FORBIDDEN, safe=False)
