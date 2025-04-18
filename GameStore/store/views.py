from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib import messages
from .services.rawg import get_games
from django.http import JsonResponse
from .forms import RegisterForm, LoginForm

User = get_user_model()

# Create your views here.
def index(request):

    context = {'title': 'GameStore - Главная'}
    
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

def game_list(request):
    games = get_games()
    return JsonResponse(games, safe=False)