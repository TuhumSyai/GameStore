"""
URL configuration for Blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views

from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'games', views.GameViewSet, basename='game')
router.register(r'genres', views.GenreViewSet)
router.register(r'platforms', views.PlatformViewSet)
router.register(r'stores', views.StoreViewSet)
router.register(r'users', views.UserViewSet)


urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.loginForm, name="login"),
    path('registration/', views.regForm, name="reg"),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('game-api/', views.game_api, name="game_api"),
    path('games-list/', views.gamelist, name="gamelist"),
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),
    path('moderators/', views.moderator_panel, name='moderator_panel'),
    path('moderator/games/', views.moderator_game_panel, name='moderator_game_panel'),
    path('moderator/games/add/', views.add_game, name='add_game'),
    path('moderator/games/<int:game_id>/edit/', views.edit_game, name='edit_game'),
    path('moderator/games/<int:game_id>/delete/', views.delete_game, name='delete_game'),
    path('api/', include(router.urls)),
    path('api/search/', views.search_games, name='search_games'),
    path('profile/', views.my_profile_view, name='my_profile'),    
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/<int:user_id>/', views.profile_view, name='profile')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)