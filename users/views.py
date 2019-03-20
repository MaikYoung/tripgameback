from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from notifications.models import Notification
from users.models import User
from users.serializers import UserSerializer, UserDetailSerializer, UserCreateSerializer, \
    UserUploadProfilePicSerializer, FollowerListSerializer, FollowingListSerializer


class UsersList(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.request.GET.get('username', None)
        if username is not None:
            return User.objects.filter(username=username).order_by('username')
        else:
            return User.objects.all().order_by('-trip_level')


class CreateUsers(APIView):
    permission_classes = []

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.validated_data, status=status.HTTP_201_CREATED, safe=False)
        else:
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)


class DetailUser(APIView):
    """
    Usr detail, update user and delete user
    """
    queryset = User.objects.all()

    def get(self, request, pk):
        user = get_object_or_404(queryset=self.queryset, id=pk)
        serializer = UserDetailSerializer(user)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    def put(self, request, pk):
        if request.user.id == pk:
            user = get_object_or_404(queryset=self.queryset, id=request.user.id)
            serializer = UserCreateSerializer(instance=user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse({'id': serializer.data.get('id')},  status=status.HTTP_200_OK, safe=False)
            else:
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)
        else:
            response = 'Not Authorized'
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST, safe=False)

    def delete(self, request, pk):
        if request.user.id == pk:
            user = get_object_or_404(queryset=self.queryset, id=request.user.id)
            user.delete()
            response = 'User deleted correctly'
            return JsonResponse(response, status=status.HTTP_204_NO_CONTENT, safe=False)
        else:
            response = 'Not Authorized'
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST, safe=False)


class UploadProfilePic(APIView):
    """
    Upload url to profile_pic of the user
    """
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
            # notification to target user new follower
            Notification.create_notification(to_user=target_user, from_user=request.user.id, type='0')
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


class UserDeleteFollower(APIView):
    """
    Delete user from followers list
    """
    queryset = User.objects.all()

    def post(self, request, pk):
        from_user = get_object_or_404(queryset=self.queryset, id=request.user.id)
        target_user = get_object_or_404(queryset=self.queryset, id=pk)
        if from_user:
            if pk in from_user.followers:
                from_user.followers.remove(pk)
                from_user.save()
                delete_follower = True
                if target_user and delete_follower:
                    target_user.following.remove(request.user.id)
                    target_user.save()
                    delete_following = True
                    if delete_follower and delete_following:
                        response = True
                        return JsonResponse(response, status=status.HTTP_200_OK, safe=False)
                else:
                    response = 'User is not in the following list'
                    return JsonResponse(data=response, status=status.HTTP_400_BAD_REQUEST, safe=False)
            else:
                response = 'User is not in the follower list'
                return JsonResponse(data=response, status=status.HTTP_400_BAD_REQUEST, safe=False)


class ListFollowersByUser(ListAPIView):
    serializer_class = FollowerListSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = get_object_or_404(User.objects.all(), id=self.request.user.id)
        return user.followers


class ListFollowingByUser(ListAPIView):
    serializer_class = FollowingListSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = get_object_or_404(User.objects.all(), id=self.request.user.id)
        return user.following
