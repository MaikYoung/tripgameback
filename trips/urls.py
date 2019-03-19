from django.urls import path

from trips.views import TripListPaginated, TripDetail, AddTripMate, DeleteTripMate, UploadPictureTrip, \
    DeletePictureTrip, VerifyTrip, TripCreate, LikeTrip, UnLikeTrip, ReportTrip

urlpatterns = [
    path('v1/trips', TripListPaginated.as_view()),
    path('v1/tripcreate', TripCreate.as_view()),
    path('v1/trip/<int:pk>', TripDetail.as_view()),
    path('v1/trip/<int:pk>/addmate/<int:user>', AddTripMate.as_view()),
    path('v1/trip/<int:pk>/deletemate/<int:user>', DeleteTripMate.as_view()),
    path('v1/trip/<int:pk>/uploadimage', UploadPictureTrip.as_view()),
    path('v1/trip/<int:pk>/deleteimage/<int:index>', DeletePictureTrip.as_view()),
    path('v1/trip/<int:pk>/verify', VerifyTrip.as_view()),
    path('v1/trip/<int:pk>/like', LikeTrip.as_view()),
    path('v1/trip/<int:pk>/unlike', UnLikeTrip.as_view()),
    path('v1/trip/<int:pk>/report', ReportTrip.as_view()),
]
