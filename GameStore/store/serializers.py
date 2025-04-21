from rest_framework import serializers
from .models import Game, Genre, Platform, Store, CustomUser

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name']

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'domain']

class GameSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    platforms = PlatformSerializer(many=True)
    stores = StoreSerializer(many=True)

    class Meta:
        model = Game
        fields = ['id', 'name', 'description', 'released', 'rating', 'rawg_id', 'background_image', 'genres', 'platforms', 'stores']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'birthdate', 'avatar', 'is_active', 'is_staff', 'is_moderator']
