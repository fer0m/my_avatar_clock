from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest

from .settings import API_ID, API_HASH


async def change_photo():
    client = TelegramClient('anon', API_ID, API_HASH)
    await client.connect()
    channel_entity = await client.get_me(input_peer=True)
    current_photo = await client.get_profile_photos(channel_entity)
    await client(DeletePhotosRequest(current_photo))
    await client.upload_file(file='pil_text.png')
    await client(UploadProfilePhotoRequest(await client.upload_file('pil_text.png')))
    await client.disconnect()
