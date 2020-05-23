from __future__ import absolute_import, unicode_literals

import asyncio
import os
import time

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

from .create_image import create_image
from .telegram_avatar import change_photo

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
    time.sleep(2)
    loop = asyncio.get_event_loop()  # == client.loop
    loop.run_until_complete(change_photo())


app.conf.beat_schedule = {
    "create_new_avatar": {
        "task": "proj.celery.telegram_change_avatar",
        "schedule": crontab()
    }
}
