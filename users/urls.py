from django.urls import path

from users.views import ListUsers, DetailUser

urlpatterns = [
    path(r'v1/users', ListUsers.as_view()),
    path(r'v1/user/<int:pk>', DetailUser.as_view())
]