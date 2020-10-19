import math
import random
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

CURRENT_FONT = f"{settings.FONT_DIR}/orange juice 2.0.ttf"


class AvatarCreator:

    @classmethod
    def create_image(cls) -> None:
        """
            Create image for telegram avatar.
        """
        width, height = 500, 500

        canvas = cls.create_canvas(width, height)
        cls.draw_time_on_canvas(image=canvas)

        canvas.save(settings.PICTURE_NAME)

    @classmethod
    def create_canvas(cls, width, height):
        img_size = (width, height)

        image = Image.new('RGB', img_size)

        center_color = [random.randint(0, 150), random.randint(0, 150), random.randint(0, 150)]
        corner_color = [random.randint(100, 240), random.randint(100, 240), random.randint(100, 240)]

        for y in range(img_size[1]):
            for x in range(img_size[0]):
                distance_to_center = math.sqrt((x - img_size[0] / 2) ** 2 + (y - img_size[1] / 2) ** 2)
                distance_to_center = float(distance_to_center) / (math.sqrt(2) * img_size[0] / 2)

                rgb = []
                for i in range(3):
                    color = int(corner_color[i] * distance_to_center + center_color[i] * (1 - distance_to_center))
                    rgb.append(color)
                rgb.append(random.randint(0, 350))

                image.putpixel((x, y), tuple(rgb))

        return image

    @classmethod
    def draw_time_on_canvas(cls, image):
        current_time = datetime.now().strftime('%H:%M')

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(CURRENT_FONT, 240)

        width_font, height_font = draw.textsize(current_time, font)
        coordinate = ((image.width - width_font) / 2, (image.height - height_font) / 2)
        draw.text(coordinate, current_time, fill=(255, 255, 255), font=font)
