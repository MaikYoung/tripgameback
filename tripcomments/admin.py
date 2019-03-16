from django.contrib import admin

from tripcomments.models import TripComments


class CommentAdmin(admin.ModelAdmin):
    model = TripComments
    list_display = ['id', 'trip', 'publisher', 'comment']


admin.site.register(TripComments, CommentAdmin)
