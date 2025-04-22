from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from django.contrib.auth import password_validation
from .models import Game, CustomUser
import datetime

User = get_user_model()


class RegisterForm(forms.ModelForm):

    
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        min_length=8,
        help_text="Минимум 8 символов"
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput
    )
    agree = forms.BooleanField(
        label="Я принимаю политику конфиденциальности",
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'birthdate', 'password', 'password2', 'agree']
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return username

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate:
            today = datetime.date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            if age < 13:
                raise ValidationError("Регистрация доступна с 13 лет.")
        return birthdate

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            self.add_error('password2', "Пароли не совпадают.")

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Логин',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите логин',
            'autocomplete': 'username',
        })
    )
    password = forms.CharField(
        required=True,
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль',
            'autocomplete': 'current-password',
        })
    )

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'description', 'released', 'rating', 'rawg_id', 'background_image', 'genres', 'platforms', 'stores']
        widgets = {
            'genres': forms.CheckboxSelectMultiple,
            'platforms': forms.CheckboxSelectMultiple,
            'stores': forms.CheckboxSelectMultiple,
        }

class ProfileUpdateForm(forms.ModelForm):
    current_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput,
        required=False
    )
    new_password = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput,
        required=False
    )
    confirm_password = forms.CharField(
        label='Подтвердите новый пароль',
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'birthdate', 'avatar', 'bio']

        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Расскажите немного о себе...',
                'style': 'resize: vertical; max-height: 200px; background-color: #1e1e22; color: white; border: none; padding: 10px; border-radius: 10px;',
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password or confirm_password:
            if not current_password:
                raise ValidationError("Введите текущий пароль для смены пароля.")
            if not self.user.check_password(current_password):
                raise ValidationError("Текущий пароль неверен.")
            if new_password != confirm_password:
                raise ValidationError("Новый пароль и подтверждение не совпадают.")
            password_validation.validate_password(new_password, self.user)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user