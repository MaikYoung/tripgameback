from django.urls import path

from medals.views import ListMedals

urlpatterns = [
    path('v1/medals', ListMedals.as_view())
]