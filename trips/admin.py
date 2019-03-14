from django.contrib import admin

from trips.models import Trip


class TripAdmin(admin.ModelAdmin):
    model = Trip
    list_display = ['id', 'owner', 'mates', 'from_to', 'destiny', 'kms', 'verified']


admin.site.register(Trip, TripAdmin)
