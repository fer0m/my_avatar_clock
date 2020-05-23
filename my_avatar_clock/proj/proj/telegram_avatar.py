from telethon import TelegramClient
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest

from .settings import API_ID, API_HASH, PHONE_NUMBER, PICTURE_NAME


async def change_photo():
    client = TelegramClient('anon', API_ID, API_HASH)
    await client.connect()
    channel_entity = await client.get_me(input_peer=True)

    if not await client.is_user_authorized():
        # If you start your app first time, telegram send secret code
        # on your phone_number.
        # Write your code here, and restart you app, will be create
        # telegram session. And restart again.
        await client.send_code_request(PHONE_NUMBER)
        await client.sign_in(PHONE_NUMBER, "Enter_here_you_code")

    current_photo = await client.get_profile_photos(channel_entity)
    await client(DeletePhotosRequest(current_photo))
    await client.upload_file(file=PICTURE_NAME)
    await client(UploadProfilePhotoRequest(await client.upload_file(PICTURE_NAME)))
    await client.disconnect()
