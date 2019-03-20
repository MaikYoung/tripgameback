from django.urls import path

from trips.views import TripListPaginated, TripDetail, AddTripMate, DeleteTripMate, UploadPictureTrip, \
    DeletePictureTrip, VerifyTrip, TripCreate, LikeTrip, UnLikeTrip, ReportTrip, TripsByUserFollowing

urlpatterns = [
    path('v1/trips', TripListPaginated.as_view()),
    path('v1/trip_create', TripCreate.as_view()),
    path('v1/trip/<int:pk>', TripDetail.as_view()),
    path('v1/trip/<int:pk>/add_mate/<int:user>', AddTripMate.as_view()),
    path('v1/trip/<int:pk>/delete_mate/<int:user>', DeleteTripMate.as_view()),
    path('v1/trip/<int:pk>/upload_image', UploadPictureTrip.as_view()),
    path('v1/trip/<int:pk>/delete_image/<int:index>', DeletePictureTrip.as_view()),
    path('v1/trip/<int:pk>/verify', VerifyTrip.as_view()),
    path('v1/trip/<int:pk>/like', LikeTrip.as_view()),
    path('v1/trip/<int:pk>/unlike', UnLikeTrip.as_view()),
    path('v1/trip/<int:pk>/report', ReportTrip.as_view()),
    path('v1/trips_following', TripsByUserFollowing.as_view()),
]
