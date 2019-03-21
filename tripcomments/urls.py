from django.urls import path

from tripcomments.views import ListComments, CreateUpdateComment

urlpatterns = [
    path('v1/comments/<int:trip>', ListComments.as_view()),
    path('v1/comment/<int:trip>/<int:pk>', CreateUpdateComment.as_view()),
]