from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib import messages
from .services.rawg import get_games
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm
from .models import Game, Genre
import random
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

User = get_user_model()

# Create your views here.
def index(request):
    random_games = Game.objects.filter(background_image__isnull=False).order_by('?')[:7]

    if not random_games.exists():
        messages.warning(request, 'Нет доступных игр для отображения.')

    banner_game = random_games[0] if random_games else None

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
        'games_data': games_data,
        'banner_game': banner_game,
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

    # Пагинация: 12 игр на страницу
    paginator = Paginator(games, 15)
    try:
        games_page = paginator.page(page)
    except PageNotAnInteger:
        games_page = paginator.page(1)
    except EmptyPage:
        games_page = paginator.page(paginator.num_pages)

    context = {
        'title': 'GameStore - Игры',
        'games': games_page,  # это page-объект
        'genres': Genre.objects.all(),
        'selected_genres': list(map(int, selected_genres)),
        'sort_option': sort_option,
        'paginator': paginator,
        'page_obj': games_page,
    }

    return render(request, 'store/games-list.html', context)

def game_detail(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    context = {
        'title': f"GameStore - {game.name}",
        'game': game
    }

    return render(request, 'store/game-detail.html', context)