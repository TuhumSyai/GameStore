from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем default настройки Django для Celery.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GameStore.settings')

app = Celery('GameStore')

# Настройки для Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически ищем задачи в приложениях Django
app.autodiscover_tasks()
