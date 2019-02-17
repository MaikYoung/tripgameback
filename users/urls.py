from django.urls import path, include

from users.views import ListUsers, DetailUser

urlpatterns = [
    path(r'v1/users', ListUsers.as_view()),
    path(r'v1/user/<int:pk>', DetailUser.as_view()),
    path(r'v1/user_auth/', include('rest_auth.urls')),
]