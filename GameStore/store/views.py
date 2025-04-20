from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .services.rawg import get_games
from .forms import RegisterForm, LoginForm, GameForm
from .models import Game, Genre, CustomUser

from django.db.models import Q

import random

User = get_user_model()


# Главная страница
def index(request):
    random_games = Game.objects.filter(background_image__isnull=False).order_by('?')[:7]

    if not random_games.exists():
        messages.warning(request, 'Нет доступных игр для отображения.')

    banner_game = random_games[0] if random_games else None

    games_data = [
        {
            'id': game.id,
            'name': game.name,
            'released': str(game.released) if game.released else 'Без даты релиза',
            'background_image': game.background_image
        }
        for game in random_games
    ]

    context = {
        'title': 'GameStore - Главная',
        'random_games': random_games,
        'games_data': games_data,
        'banner_game': banner_game,
    }

    return render(request, 'store/index.html', context)


# Проверка на администратора
def is_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_admin)
def moderator_panel(request):
    query = request.GET.get('q', '')
    users = CustomUser.objects.filter()

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        user = get_object_or_404(CustomUser, id=user_id)
        user.is_moderator = (action == 'grant')
        user.save()

        return redirect('moderator_panel')

    context = {
        'title': 'Управление модераторами',
        'users': users,
    }
    return render(request, 'store/Moderator/moderator_panel.html', context)


# Проверка на модератора или администратора
def is_moderator(user):
    return user.is_authenticated and (user.is_moderator or user.is_superuser)


# Панель модерации игр
@user_passes_test(is_moderator)
def moderator_game_panel(request):
    query = request.GET.get('q', '')
    games = Game.objects.all()

    if query:
        games = games.filter(name__icontains=query)

    context = {
        'title': 'Модерация игр',
        'games': games,
    }
    return render(request, 'store/Moderator/moderator_game_panel.html', context)


# Редактирование игры
@user_passes_test(is_moderator)
def edit_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('moderator_game_panel')
    else:
        form = GameForm(instance=game)

    context = {
        'title': 'Редактирование игры',
        'form': form,
    }
    return render(request, 'store/Moderator/edit_game.html', context)


# Удаление игры
@user_passes_test(is_moderator)
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == 'POST':
        game.delete()
        return redirect('moderator_game_panel')

    context = {
        'title': 'Удаление игры',
        'game': game,
    }
    return render(request, 'store/Moderator/delete_game.html', context)


# Добавление игры вручную
@user_passes_test(is_moderator)
def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('moderator_game_panel')
    else:
        form = GameForm()

    context = {
        'title': 'Добавить игру',
        'form': form,
    }
    return render(request, 'store/Moderator/add_game.html', context)


# Авторизация пользователя
def loginForm(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Неверный логин или пароль')

    context = {
        'title': 'GameStore - Авторизация',
        'form': form,
    }
    return render(request, 'store/login.html', context)


# Регистрация пользователя
def regForm(request):
    context = {'title': 'GameStore - Регистрация'}

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/')
        else:
            context['form'] = form
            return render(request, 'store/reg.html', context)

    context['form'] = RegisterForm()
    return render(request, 'store/reg.html', context)


# Получение игр через RAWG API
def game_api(request):
    games = get_games()
    return JsonResponse(games, safe=False)


# Список игр с фильтрацией и сортировкой
def gamelist(request):
    sort_option = request.GET.get('sort', 'added')
    selected_genres = request.GET.getlist('genres')
    page = request.GET.get('page', 1)

    games = Game.objects.all()

    if selected_genres:
        games = games.filter(genres__id__in=selected_genres).distinct()

    if not games.exists():
        messages.warning(request, 'В базе данных нет игр по выбранным фильтрам.')

    if sort_option == 'added':
        games = games.order_by('-id')
    elif sort_option == '-released':
        games = games.order_by('-released')
    elif sort_option == '-metacritic':
        games = games.order_by('-rating')

    paginator = Paginator(games, 15)
    try:
        games_page = paginator.page(page)
    except PageNotAnInteger:
        games_page = paginator.page(1)
    except EmptyPage:
        games_page = paginator.page(paginator.num_pages)

    context = {
        'title': 'GameStore - Игры',
        'games': games_page,
        'genres': Genre.objects.all(),
        'selected_genres': list(map(int, selected_genres)),
        'sort_option': sort_option,
        'paginator': paginator,
        'page_obj': games_page,
    }

    return render(request, 'store/games-list.html', context)


# Детальная страница игры
def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    context = {
        'title': f"GameStore - {game.name}",
        'game': game,
    }
    return render(request, 'store/game-detail.html', context)
