import requests
from store.models import Game, Genre, Platform, Store

API_KEY = '2b27fe820d7a4aac84a82ad564f939f3'  # Замените на ваш API-ключ от RAWG
BASE_URL = 'https://api.rawg.io/api/games'

def get_data_from_rawg(page=1):
    """
    Запрашивает данные с RAWG API, возвращает JSON.
    """
    params = {
        'key': API_KEY,
        'page_size': 100,  # Количество игр на странице
        'page': page  # Номер страницы
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()  # возвращает данные в формате JSON

def update_games_from_api():
    page = 1
    while True:
        data = get_data_from_rawg(page)
        games = data['results']

        for game in games:
            name = game.get('name')
            released = game.get('released')
            rating = game.get('rating')
            description = game.get('description', '')
            background_image = game.get('background_image')  # Добавляем обложку

            platforms = game.get('platforms', [])
            genres = game.get('genres', [])
            stores = game.get('stores', [])

            game_obj, created = Game.objects.update_or_create(
                rawg_id=game['id'],
                defaults={
                    'name': name,
                    'released': released,
                    'rating': rating,
                    'description': description,
                    'background_image': background_image
                }
            )

            # Жанры
            for genre in genres:
                genre_obj, _ = Genre.objects.get_or_create(name=genre['name'])
                game_obj.genres.add(genre_obj)

            # Платформы
            for platform in platforms:
                platform_obj, _ = Platform.objects.get_or_create(name=platform['platform']['name'])
                game_obj.platforms.add(platform_obj)

            # Магазины
            for store in stores:
                store_obj, _ = Store.objects.get_or_create(
                    name=store['store']['name'],
                    domain=store['store']['domain']
                )
                game_obj.stores.add(store_obj)

        if len(games) < 100:
            break

        page += 1


import redis

def connect_to_redis():
    r = redis.Redis(
        host='redis-12310.crce198.eu-central-1-3.ec2.redns.redis-cloud.com',
        port=12310,
        decode_responses=True,
        username='default',
        password='gbdQVm9isCgQUn2VfS2SKcC4ZPcKNaFR'
    )
    return r

def cache_data(data):
    r = connect_to_redis()
    r.set('game_data', data)  # Кэшируем данные
