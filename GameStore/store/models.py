from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=255)
    released = models.DateField()
    rating = models.FloatField()
    description = models.TextField()
    rawg_id = models.IntegerField(unique=True)  # Уникальный идентификатор игры

    def __str__(self):
        return self.name
