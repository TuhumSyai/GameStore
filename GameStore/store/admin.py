from django.contrib import admin
from .models import Game, Platform, Genre, Store, CustomUser

admin.site.register(Game)
admin.site.register(Platform)
admin.site.register(Genre)
admin.site.register(Store)

from django.contrib.auth.admin import UserAdmin

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_active']
    search_fields = ['email', 'username']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'birthdate')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'birthdate', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )