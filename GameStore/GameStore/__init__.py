from __future__ import absolute_import, unicode_literals

# Это помогает Celery запускаться при старте Django
from .celery import app as celery_app

__all__ = ('celery_app',)
