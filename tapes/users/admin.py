from django.contrib import admin

from .models import User


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'username',
        'full_name',
        'date_joined'
    )


admin.site.register(User, CustomUserAdmin)
