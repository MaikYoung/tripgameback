from django.contrib import admin

from points.models import Point


class PointAdmin(admin.ModelAdmin):
    model = Point
    list_display = ['id', 'owner', 'points']


admin.site.register(Point, PointAdmin)
