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
    background_image = models.URLField(blank=True, null=True)  # Обложка игры
    genres = models.ManyToManyField(Genre)
    platforms = models.ManyToManyField(Platform)
    stores = models.ManyToManyField(Store)
    price_kzt = models.DecimalField(max_digits=10, decimal_places=2, default=1000)

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
        user.is_moderator = True
        user.save(using=self._db)
        return user


from django.conf import settings

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    bio = models.TextField(blank=True, null=True)   
    birthdate = models.DateField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        default='avatars/default.png',
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'birthdate']

    def __str__(self):
        return self.username
    

class Comment(models.Model):
    game = models.ForeignKey('Game', related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Комментарий от {self.user.username} для {self.game.name}"
    
class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='purchases')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='purchases')
    purchase_date = models.DateTimeField(auto_now_add=True)
    price_kzt = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'game')  # пользователь не может купить одну игру дважды

    def __str__(self):
        return f"{self.user.username} купил {self.game.name} за {self.price_kzt}₸"