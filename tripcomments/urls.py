from django.urls import path

from tripcomments.views import ListComments, CreateUpdateComment

urlpatterns = [
    path('v1/<int:trip>/comments', ListComments.as_view()),
    path('v1/<int:trip>/comment/<int:pk>', CreateUpdateComment.as_view()),
]