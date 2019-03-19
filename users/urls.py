from django.urls import path, include


from users.views import CreateUsers, DetailUser, UploadProfilePic, UserAddFollowing, UserDeleteFollowing, \
    UserDeleteFollower, ListFollowersByUser, ListFollowingByUser, UsersList

urlpatterns = [
    path(r'v1/users', UsersList.as_view()),
    path(r'v1/usercreate', CreateUsers.as_view()),
    path(r'v1/user/<int:pk>', DetailUser.as_view()),
    path(r'v1/user/followers', ListFollowersByUser.as_view()),
    path(r'v1/user/following', ListFollowingByUser.as_view()),
    path(r'v1/user_auth/', include('rest_auth.urls')),
    path(r'v1/user/uploadimage', UploadProfilePic.as_view()),
    path(r'v1/user/addfollowing/<int:pk>', UserAddFollowing.as_view()),
    path(r'v1/user/deletefollowing/<int:pk>', UserDeleteFollowing.as_view()),
    path(r'v1/user/deletefollower/<int:pk>', UserDeleteFollower.as_view())
]