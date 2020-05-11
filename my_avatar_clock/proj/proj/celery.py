from __future__ import absolute_import, unicode_literals

import asyncio
import os
import time

from celery import Celery

from .create_image import create_image
from .telegram_avatar import change_photo

# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

app = Celery('proj')

#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.timezone = 'Europe/Moscow'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(50.0, telegram_change_avatar.s(), expires=10)


@app.task
def telegram_change_avatar():
    create_image()
    time.sleep(2)
    loop = asyncio.get_event_loop()  # == client.loop
    loop.run_until_complete(change_photo())
