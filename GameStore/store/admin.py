from django.contrib import admin
from .models import Game, Platform, Genre, Store, CustomUser, Comment, Purchase
from django.db.models import Count, Sum
from django.utils.html import format_html

admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Store)
admin.site.register(Comment)

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

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'released', 'rating', 'price_kzt', 'total_purchases')

    def total_purchases(self, obj):
        return obj.purchases.count()
    total_purchases.short_description = "Кол-во покупок"

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'purchase_date', 'price_kzt')

    def total_revenue(self, request, queryset):
        total = queryset.aggregate(Sum('price_kzt'))['price_kzt__sum'] or 0
        self.message_user(request, f'Общая выручка: {total} ₸')
    actions = ['total_revenue']