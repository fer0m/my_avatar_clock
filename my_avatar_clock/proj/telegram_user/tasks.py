import asyncio
import logging
from datetime import datetime
from .create_image import AvatarCreator
from .telegram_avatar import change_photo, get_account
from config.celery_app import app

logger = logging.getLogger(__name__)


@app.task
def telegram_change_avatar():
    AvatarCreator().create_image()

    account = get_account()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(change_photo(account))
    logger.info(f'Avatar is changed in {datetime.now()}')
