from django.urls import path

from tripcomments.views import ListComments

urlpatterns = [
    path('v1/<int:pk>/comments', ListComments.as_view()),
]