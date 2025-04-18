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
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.loginForm, name="login"),
    path('registration/', views.regForm, name="reg"),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('game-api/', views.game_api, name="game_api"),
    path('games-list/', views.gamelist, name="gamelist"),
]
