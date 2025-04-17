from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Genre(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Platform(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Store(models.Model):
    name = models.CharField(max_length=255)
    domain = models.URLField()

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    released = models.DateField()
    rating = models.FloatField()
    rawg_id = models.IntegerField(unique=True)  # Уникальный идентификатор игры
    genres = models.ManyToManyField(Genre)
    platforms = models.ManyToManyField(Platform)
    stores = models.ManyToManyField(Store)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, birthdate, password=None):
        if not email:
            raise ValueError('У пользователя должен быть email')
        if not username:
            raise ValueError('У пользователя должно быть имя')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, birthdate=birthdate)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, birthdate, password):
        user = self.create_user(email, username, birthdate, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    birthdate = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'birthdate']

    def __str__(self):
        return self.email