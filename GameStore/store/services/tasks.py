from celery import shared_task
from store.services.utils import update_games_from_api, connect_to_redis

@shared_task
def update_games():
    update_games_from_api()
    return "Games updated successfully"

@shared_task
def set_redis_value():
    r = connect_to_redis()
    r.set('foo', 'bar')
    return r.get('foo')