from django.db import models

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
