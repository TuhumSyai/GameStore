from .utils import update_games_from_api

# Вы можете вызвать эту функцию для обновления данных
update_games_from_api()

from celery import shared_task
from .utils import connect_to_redis  # импортируем функцию подключения к Redis

@shared_task
def set_redis_value():
    r = connect_to_redis()  # подключаемся к Redis
    r.set('foo', 'bar')  # записываем значение в Redis
    result = r.get('foo')  # получаем значение из Redis
    print(result)  # выводим результат
    return result

from celery import shared_task
from .utils import update_games_from_api

@shared_task
def update_games():
    """
    Задача для обновления данных об играх через API.
    """
    update_games_from_api()  # вызов функции для обновления данных
    return "Games updated successfully"
