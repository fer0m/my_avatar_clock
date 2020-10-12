import random
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from django.conf import settings

CURRENT_FONT = f"{settings.FONT_DIR}/orange juice 2.0.ttf"


def create_image() -> None:
    """
        Create image for telegram avatar.
    """

    msg = datetime.now().strftime('%H:%M')

    W, H = (500, 500)
    color_2 = random.randint(100, 200)
    color_3 = random.randint(100, 200)
    img = Image.new('RGB', (W, H), color=(100, color_2, color_3))

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(CURRENT_FONT, 240)
    w, h = draw.textsize(msg, font)
    draw.text(((W - w) / 2, (H - h) / 2), msg, fill=(255, 255, 0), font=font)

    img.save(settings.PICTURE_NAME)