from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['id', 'username', 'first_name', 'last_name', 'email']


admin.site.register(User, UserAdmin)