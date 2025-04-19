from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib import messages
from .services.rawg import get_games
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm
from .models import Game
import random
from django.db.models import Q

User = get_user_model()

# Create your views here.
def index(request):
    random_games = Game.objects.filter(background_image__isnull=False).order_by('?')[:7]

    # Делаем баннер на основе первой игры (или какой-то другой логики)
    banner_game = random_games[0] if random_games else None

    # Сериализуем нужные данные
    games_data = [
        {
            'name': game.name,
            'released': str(game.released) if game.released else 'Без даты релиза',
            'background_image': game.background_image
        }
        for game in random_games
    ]

    context = {
        'title': 'GameStore - Главная',
        'random_games': random_games,
        'games_data': games_data,  # Добавляем сериализованные данные
        'banner_game': banner_game,  # Передаем конкретную игру для баннера
    }

    return render(request, 'store/index.html', context)

def loginForm(request):
    form = LoginForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Неверный логин или пароль')

    context = {
        'form': form,
        'title': 'GameStore - Авторизация'
    }
    return render(request, 'store/login.html', context)

def regForm(request):
    context = {'title': 'GameStore - Регистрация'}

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # хэшируем пароль
            user.save()
            login(request, user)  # логиним пользователя
            return redirect('/')
        else:
            context['form'] = form
            return render(request, 'store/reg.html', context)

    form = RegisterForm()
    context['form'] = form
    return render(request, 'store/reg.html', context)

def game_api(request):
    games = get_games()
    return JsonResponse(games, safe=False)

def gamelist(request):
     context = {
         'title': 'GameStore - Игры'
     }
     
     return render(request, 'store/games-list.html', context)

