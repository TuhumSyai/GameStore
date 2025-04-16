import requests
from store.models import Game


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
    """
    Обновляет или добавляет данные о играх в базу данных.
    """
    page = 1
    while True:
        data = get_data_from_rawg(page)
        games = data['results']

        for game in games:
            # Обновляем или добавляем игру в базу данных
            game_obj, created = Game.objects.update_or_create(
                rawg_id=game['id'],
                defaults={
                    'name': game['name'],
                    'released': game['released'],
                    'rating': game['rating'],
                    'description': game['description']
                }
            )

        # Если на текущей странице нет данных, завершаем цикл
        if len(games) < 100:
            break

        page += 1  # Переход к следующей странице



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

