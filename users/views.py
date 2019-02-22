

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from notifications.models import Notification
from project.settings import NOTIFICATION_TYPES
from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer, UserCreateSerializer, \
    UserUploadProfilePicSerializer, UserFollowersSerializer


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

    def get(self, request):
        user = get_object_or_404(queryset=self.queryset, id=request.user.id)
        serializer = UserDetailSerializer(user)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    def put(self, request):
        user = get_object_or_404(queryset=self.queryset, id=request.user.id)
        serializer = UserCreateSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse({'id': serializer.data.get('id')},  status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    def delete(self, request):
        # TODO: Mirar por que 'ConnectionResetError: [Errno 104] Connection reset by peer' despues de borrar un user
        if request.user.is_superuser:
            user = get_object_or_404(queryset=self.queryset, id=request.user.id)
            user.delete()
            response = 'User deleted correctly'
            return JsonResponse(response, status=status.HTTP_204_NO_CONTENT, safe=False)
        else:
            response = 'Not Authorized'
            return JsonResponse(response, status=status.HTTP_403_FORBIDDEN, safe=False)


class UploadProfilePic(APIView):
    queryset = User.objects.all()

    def put(self, request, pk):
        user = get_object_or_404(queryset=self.queryset, id=pk)
        serializer = UserUploadProfilePicSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)


class UserFollowers(APIView):
    queryset = User.objects.all()

    def put(self, request, to_user):
        """add following"""
        from_user = get_object_or_404(queryset=self.queryset, id=request.user.id)
        obj = {
            'following': [to_user]
        }
        serializer = UserFollowersSerializer(instance=from_user, data=obj, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        """add follower"""
        target = get_object_or_404(queryset=self.queryset, id=to_user)
        obj_2 = {
            'follower': [request.user.id]
        }
        serializer = UserFollowersSerializer(instance=target, data=obj_2, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return JsonResponse(from_user, status=status.HTTP_200_OK)
