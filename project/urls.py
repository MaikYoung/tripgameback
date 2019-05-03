
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('files.urls')),
    path('api/', include('notifications.urls')),
    path('api/', include('trips.urls')),
    path('api/', include('points.urls')),
    path('api/', include('tripcomments.urls')),
    path('api/', include('medals.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
