from __future__ import absolute_import, unicode_literals

import logging
from datetime import datetime

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proj.settings")
django.setup()

import asyncio
import time

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

from .create_image import create_image
from .telegram_avatar import change_photo, get_account

logger = logging.getLogger(__name__)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj')

#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
app.conf.timezone = 'Europe/Moscow'
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def telegram_change_avatar():
    create_image()
    account = get_account()
    time.sleep(2)
    loop = asyncio.get_event_loop()  # == client.loop
    loop.run_until_complete(change_photo(account))
    logger.debug(f'Avatar is changed in {datetime.now()}')


app.conf.beat_schedule = {
    "create_new_avatar": {
        "task": "telegram_user.celery.telegram_change_avatar",
        "schedule": crontab()
    }
}
