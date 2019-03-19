from django.contrib import admin

from medals.models import Medals


class MedalAdmin(admin.ModelAdmin):
    model = Medals
    list_display = ['owner', 'ski', 'trekking', 'beach', 'cultural', 'festival', 'party', 'surf', 'gastronomic']


admin.site.register(Medals, MedalAdmin)
