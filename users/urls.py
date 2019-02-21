from django.urls import path, include

from users.views import ListUsers, DetailUser, UploadProfilePic, UserFollowers

urlpatterns = [
    path('v1/users', ListUsers.as_view()),
    path('v1/user/<int:pk>', DetailUser.as_view()),
    path('v1/user_auth/', include('rest_auth.urls')),
    path('v1/user/<int:pk>/uploadimage', UploadProfilePic.as_view()),
    path('v1/user/<int:to_user>/new_follower', UserFollowers.as_view())
]