from django.urls import path

from notifications.views import NotificationList

urlpatterns = [
    path('v1/notifications', NotificationList.as_view()),
]
