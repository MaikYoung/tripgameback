from django.urls import path

from points.views import PointsUserDetail

urlpatterns = [
    path('v1/points', PointsUserDetail.as_view()),
]