import logging
from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest

from django.conf import settings
from .models import TelegramUser

logger = logging.getLogger(__name__)


async def change_photo(tg_user):
    client = TelegramClient('anon', tg_user.api_id, tg_user.api_hash)

    try:
        await client.connect()
        channel_entity = await client.get_me(input_peer=True)

        if not await client.is_user_authorized():
            await client.send_code_request(tg_user.phone)
            await client.sign_in(tg_user.phone, tg_user.secret_tg_key)

        if await client.is_user_authorized():
            current_photo = await client.get_profile_photos(channel_entity)
            await client(DeletePhotosRequest(current_photo))
            await client.upload_file(file=settings.PICTURE_NAME)
            await client(UploadProfilePhotoRequest(await client.upload_file(settings.PICTURE_NAME)))

        await client.disconnect()

    except Exception:
        await client.disconnect()
        logger.exception(msg='Exception!')


def get_account():
    return TelegramUser.objects.first()
