import requests
from store.models import Game, Genre, Platform, Store

API_KEY = '2b27fe820d7a4aac84a82ad564f939f3' 
BASE_URL = 'https://api.rawg.io/api/games'

def get_data_from_rawg(page):
    """
    Запрашивает данные с RAWG API, возвращает JSON.
    """
    params = {
        'key': API_KEY,
        'page_size': 40,  # Количество игр на странице
        'page': page  # Номер страницы
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()  # возвращает данные в формате JSON

def update_games_from_api():
    max_pages = 10
    page = 1
    while page <= max_pages:
        data = get_data_from_rawg(page)
        games = data.get('results', [])

        for game in games:
            name = game.get('name')
            released = game.get('released')
            if not released:
                continue
            rating = game.get('rating')
            if not rating:
                continue
            description = game.get('description', '')
            background_image = game.get('background_image')

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

            # ManyToMany поля
            game_obj.genres.clear()
            for genre in genres:
                genre_obj, _ = Genre.objects.get_or_create(name=genre['name'])
                game_obj.genres.add(genre_obj)

            game_obj.platforms.clear()
            for platform in platforms:
                platform_obj, _ = Platform.objects.get_or_create(name=platform['platform']['name'])
                game_obj.platforms.add(platform_obj)

            game_obj.stores.clear()
            for store in stores:
                store_obj, _ = Store.objects.get_or_create(
                    name=store['store']['name'],
                    domain=store['store']['domain']
                )
                game_obj.stores.add(store_obj)

        # Переход к следующей странице, если есть
        if not data.get('next'):
            break
        page += 1


import redis

def connect_to_redis():
    r = redis.Redis(
        host='redis-13415.crce198.eu-central-1-3.ec2.redns.redis-cloud.com',
        port=13415,
        decode_responses=True,
        username='default',
        password='Ze7ee0H2CecRHgjQdCEEyPBb6xB03xdO'
    )
    return r

def cache_data(data):
    r = connect_to_redis()
    r.set('game_data', data)  # Кэшируем данные
