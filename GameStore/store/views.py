from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib import messages
from .services.rawg import get_games
from django.http import JsonResponse

User = get_user_model()

# Create your views here.
def index(request):

    context = {'title': 'GameStore - Главная'}
    
    return render(request, 'store/index.html', context)

def loginForm(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Ищем пользователя по email
        try:
            from .models import CustomUser
            user = CustomUser.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except CustomUser.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('/')  # замените на нужный URL
        else:
            messages.error(request, 'Неверный email или пароль')

    context = {'title': 'GameStore - Авторизация'}

    return render(request, 'store/login.html', context)

def regForm(request):

    context = {'title': 'GameStore - Регистрация'}

    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        birthdate = request.POST.get('birthdate')  # формат: 'YYYY-MM-DD'
        password = request.POST.get('password')

        # Проверка, существует ли пользователь с таким email
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
            return render(request, 'store/reg.html', context)

        # Создание нового пользователя
        user = User.objects.create_user(
            email=email,
            username=username,
            birthdate=birthdate,
            password=password
        )

        login(request, user)  # автоматически логиним после регистрации
        return redirect('/')  # перенаправление после регистрации

    return render(request, 'store/reg.html', context)

def game_list(request):
    games = get_games()
    return JsonResponse(games, safe=False)