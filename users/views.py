import json

from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer, UserCreateSerializer, \
    UserUploadProfilePicSerializer


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

    def put(self, request):
        user = get_object_or_404(queryset=self.queryset, id=request.user.id)
        serializer = UserUploadProfilePicSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)


class UserAddFollowing(APIView):
    """
    ADD pk to following of the request user amd add to pk followers the user of the request
    """
    queryset = User.objects.all()

    def post(self, request, pk):
        from_user = get_object_or_404(queryset=self.queryset, id=request.user.id)
        target_user = get_object_or_404(queryset=self.queryset, id=pk)
        if from_user:
            if pk in from_user.following:
                response = 'User is already followed'
                return JsonResponse(data=response, status=status.HTTP_400_BAD_REQUEST, safe=False)
            else:
                from_user.following.append(pk)
                from_user.save()
                add_following = True
                if target_user and add_following:
                    if request.user.id in target_user.followers:
                        response = 'User is already a follower'
                        return JsonResponse(data=response, status=status.HTTP_400_BAD_REQUEST, safe=False)
                    else:
                        target_user.followers.append(request.user.id)
                        target_user.save()
                        add_follower = True
        if add_following and add_follower:
            response = True
            return JsonResponse(response, status=status.HTTP_200_OK, safe=False)
        else:
            return JsonResponse(status=status.HTTP_400_BAD_REQUEST)


class UserDeleteFollowing(APIView):
    """
    Delete pk to following of the request user amd delete of the pk followers the user of the request
    """
    queryset = User.objects.all()

    def post(self, request, pk):
        from_user = get_object_or_404(queryset=self.queryset, id=request.user.id)
        target_user = get_object_or_404(queryset=self.queryset, id=pk)
        if from_user:
            if pk in from_user.following:
                from_user.following.remove(pk)
                from_user.save()
                delete_following = True
                if target_user and delete_following:
                    target_user.followers.remove(request.user.id)
                    target_user.save()
                    delete_follower = True
                    if delete_following and delete_follower:
                        response = True
                        return JsonResponse(response, status=status.HTTP_200_OK, safe=False)
                else:
                    response = 'User is not in the follower list'
                    return JsonResponse(data=response, status=status.HTTP_400_BAD_REQUEST, safe=False)
            else:
                response = 'User is not in the following list'
                return JsonResponse(data=response, status=status.HTTP_400_BAD_REQUEST, safe=False)