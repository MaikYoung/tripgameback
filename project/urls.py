
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('files.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('trips.urls')),
    path('api/', include('points.urls')),
    path('api/', include('tripcomments.urls')),
    path('api/', include('medals.urls')),
]
