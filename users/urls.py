from django.urls import path, include


from users.views import ListUsers, DetailUser, UploadProfilePic, UserAddFollowing, UserDeleteFollowing

urlpatterns = [
    path(r'v1/users', ListUsers.as_view()),
    path(r'v1/user/<int:pk>', DetailUser.as_view()),
    path(r'v1/user_auth/', include('rest_auth.urls')),
    path(r'v1/user/uploadimage', UploadProfilePic.as_view()),
    path(r'v1/user/addfollowing/<int:pk>', UserAddFollowing.as_view()),
    path(r'v1/user/deletefollowing/<int:pk>', UserDeleteFollowing.as_view()),
]