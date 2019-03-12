from django.urls import path

from trips.views import TripList, TripDetail, AddTripMate

urlpatterns = [
    path('v1/trips', TripList.as_view()),
    path('v1/trip/<int:pk>', TripDetail.as_view()),
    path('v1/trip/<int:pk>/addmate/<int:user>', AddTripMate.as_view()),
]