from __future__ import absolute_import, unicode_literals

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

app = Celery('proj')

app.conf.timezone = 'Europe/Moscow'
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS, force=True)
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    "create_new_avatar": {
        "task": "telegram_user.tasks.telegram_change_avatar",
        "schedule": crontab(),
    }
}

app.conf.task_routes = {
    'proj.telegram_user.tasks.telegram_change_avatar': {'queue': 'other'}
}
