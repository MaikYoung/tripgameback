from django.contrib import admin

from notifications.models import Notification


class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = ['to_user', 'from_user', 'type', 'trip_related', 'active']


admin.site.register(Notification, NotificationAdmin)
