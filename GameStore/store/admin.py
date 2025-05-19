from django.contrib import admin
from .models import Game, Platform, Genre, Store, CustomUser, Comment, Purchase
from django.db.models import Count, Sum
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Platform)
class PlatformAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'short_content', 'created_at')
    search_fields = ('user__username', 'game__name', 'content')
    list_filter = ('created_at', 'game', 'user')

    def short_content(self, obj):
        return obj.content[:50] + ('...' if len(obj.content) > 50 else '')
    short_content.short_description = 'Содержание'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_active']
    search_fields = ['email', 'username']
    ordering = ['email']

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'birthdate', 'bio', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined', 'last_activity')}),
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
    search_fields = ('name',)
    list_filter = ('genres', 'platforms', 'stores', 'released')

    def total_purchases(self, obj):
        return obj.purchases.count()
    total_purchases.short_description = "Кол-во покупок"


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'game', 'purchase_date', 'price_kzt')
    list_filter = ('purchase_date', 'game', 'user')
    search_fields = ('user__username', 'game__name')

    def total_revenue(self, request, queryset):
        total = queryset.aggregate(Sum('price_kzt'))['price_kzt__sum'] or 0
        self.message_user(request, f'Общая выручка: {total} ₸')

    actions = ['total_revenue']
