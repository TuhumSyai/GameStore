from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from django.views.decorators.csrf import csrf_exempt



from .services.rawg import get_games
from .forms import RegisterForm, LoginForm, GameForm, ProfileUpdateForm
from .models import Game, Genre, Platform, Store, CustomUser, Comment, Purchase

from .serializers import GameSerializer, GenreSerializer, PlatformSerializer, StoreSerializer, UserSerializer, CommentSerializer, PurchaseSerializer

from django.db.models import Q

from django.conf import settings

from django.utils.timezone import now

import requests

import math

import stripe

User = get_user_model()

import json

stripe.api_key = settings.STRIPE_SECRET_KEY




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
    context = {'title': 'GameStore - Авторизация'}

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('/')
        else:
            context['form'] = form
            return render(request, 'store/login.html', context)

    context['form'] = LoginForm()
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
    page = int(request.GET.get('page', 1))

    params = {
        'ordering': {
            'added': '-id',
            '-released': '-released',
            '-metacritic': '-rating',
        }.get(sort_option, '-id'),
        'page': page
    }

    # Добавляем жанры
    if selected_genres:
        params['genres'] = selected_genres

    print(f"Request params: {params}")  # Логируем параметры запроса

    try:
        response = requests.get('http://127.0.0.1:8000/api/games/', params=params)
        response.raise_for_status()
        data = response.json()
        print(f"Response data: {data}")  # Логируем данные из ответа API

        games_data = data.get('results', [])
        count = data.get('count', 0)
        next_page_url = data.get('next')
        prev_page_url = data.get('previous')

        # Корректно вычисляем количество страниц с использованием math.ceil()
        total_pages = math.ceil(count / 10)  # количество страниц, округляем вверх
    except requests.RequestException:
        messages.error(request, 'Не удалось получить данные из API.')
        games_data = []
        count = 0
        next_page_url = None
        prev_page_url = None
        total_pages = 1

    print(f"Total pages: {total_pages}")  # Логируем total_pages

    # Создаём page_range с учётом общей численности страниц
    page_range = range(
        max(1, page - 2),
        min(page + 3, total_pages + 1)
    )

    context = {
        'title': 'GameStore - Игры',
        'games': games_data,
        'genres': Genre.objects.all(),
        'selected_genres': list(map(int, selected_genres)),
        'sort_option': sort_option,
        'page_obj': {
            'number': page,
            'paginator': {'num_pages': total_pages},
            'has_previous': prev_page_url is not None,
            'has_next': next_page_url is not None,
            'previous_page_number': page - 1 if prev_page_url else None,
            'next_page_number': page + 1 if next_page_url else None,
        },
        'page_range': page_range
    }

    return render(request, 'store/games-list.html', context)


def game_detail(request, game_id):
    # Получаем игру через ORM
    game = get_object_or_404(Game, id=game_id)

    user_has_purchased = request.user.is_authenticated and request.user.purchases.filter(game=game).exists()

    # Обработка формы комментария
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                game=game,  # Связываем комментарий с игрой
                user=request.user,  # Связываем комментарий с текущим пользователем
                content=content,
            )
            return redirect('game_detail', game_id=game_id)  # Перенаправляем после создания комментария

    # Получаем все комментарии для игры
    comments = game.comments.all()

    context = {
        'title': f"GameStore - {game.name}",
        'game': game,
        'comments': comments,  # Передаем комментарии в контекст
        'user_has_purchased': user_has_purchased,
    }
    return render(request, 'store/game-detail.html', context)


def profile_view(request, user_id):
    user_profile = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'store/profile.html', {
        'user_profile': user_profile,
        'MEDIA_URL': settings.MEDIA_URL, 
    })

@login_required
def my_profile_view(request):
    user = request.user
    is_online = False
    if user.last_activity:
        delta = now() - user.last_activity
        is_online = delta.total_seconds() < 300

    context = {
        'title': 'Профиль',
        'user_profile': user,
        'MEDIA_URL': settings.MEDIA_URL, 
        'online_status': is_online,
    }

    return render(request, 'store/profile.html', context)

@login_required
def edit_profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён.')
            return redirect('my_profile')  # Название URL для просмотра профиля
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ProfileUpdateForm(instance=user)

    context = {
        'title': 'Редактировать профиль',
        'form': form,
        'MEDIA_URL': settings.MEDIA_URL, 
    }

    return render(request, 'store/edit_profile.html', context)


@api_view(['GET'])
def search_games(request):
    query = request.GET.get('q', '')
    if query:
        games = Game.objects.filter(name__icontains=query)[:10]
        serializer = GameSerializer(games, many=True)
        return Response(serializer.data)
    return Response([])


@login_required
@csrf_exempt
def create_checkout_session(request, game_id):
    game = Game.objects.get(id=game_id)
    price = int(game.price_kzt * 100)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'kzt',
                'unit_amount': price,
                'product_data': {
                    'name': game.name,
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
        metadata={
        'user_id': request.user.id,
        'game_id': game.id,
    }
    )

    return redirect(session.url, code=303)

def success_view(request):
    return render(request, 'store/payment/success.html')

def cancel_view(request):
    return render(request, 'store/payment/cancel.html')


@login_required
def purchases(request):
    sort_option = request.GET.get('sort', 'added')
    selected_genres = request.GET.getlist('genres')
    page = int(request.GET.get('page', 1))

    # Получаем купленные пользователем игры
    purchased_games = Game.objects.filter(purchases__user=request.user)

    # Фильтруем по жанрам
    if selected_genres:
        purchased_games = purchased_games.filter(genres__id__in=selected_genres).distinct()

    # Сортировка
    ordering = {
        'added': '-id',
        '-released': '-released',
        '-metacritic': '-rating',
    }.get(sort_option, '-id')
    purchased_games = purchased_games.order_by(ordering)

    # Пагинация
    paginator = Paginator(purchased_games, 10)
    page_obj = paginator.get_page(page)
    page_range = range(
        max(1, page_obj.number - 2),
        min(page_obj.number + 3, paginator.num_pages + 1)
    )

    context = {
        'title': 'Мои покупки',
        'purchased_games': page_obj.object_list,
        'genres': Genre.objects.all(),
        'selected_genres': list(map(int, selected_genres)),
        'sort_option': sort_option,
        'page_obj': page_obj,
        'page_range': page_range
    }

    return render(request, 'store/purchases.html', context)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    if sig_header is None:
        return HttpResponse("Missing Stripe Signature Header", status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse(f"Invalid payload: {e}", status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(f"Signature verification failed: {e}", status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})

        user_id = metadata.get('user_id')
        game_id = metadata.get('game_id')

        try:
            user = CustomUser.objects.get(id=user_id)
            game = Game.objects.get(id=game_id)
        except CustomUser.DoesNotExist:
            return HttpResponse(f"User not found: {user_id}", status=404)
        except Game.DoesNotExist:
            return HttpResponse(f"Game not found: {game_id}", status=404)

        Purchase.objects.create(
            user=user,
            game=game,
            price_kzt=game.price_kzt
        )

    return HttpResponse(status=200)

# API view for Game
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['genres', 'name']
    ordering_fields = ['released', 'rating', 'id']
    ordering = ['-id']

# API view for Genre
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUser]


# API view for Platform
class PlatformViewSet(viewsets.ModelViewSet):
    queryset = Platform.objects.all()
    serializer_class = PlatformSerializer
    permission_classes = [IsAdminUser]


# API view for Store
class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsAdminUser]


# API view for User
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAdminUser]