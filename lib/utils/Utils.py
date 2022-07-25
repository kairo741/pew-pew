from random import randint
from pygame import transform

from lib.object.Axis import Axis


class Utils:
    @staticmethod
    def scale_image(image, scale=1):
        img_size = Axis(image.get_width(), image.get_height())

        return transform.smoothscale(image, [(img_size.x * scale), (img_size.y * scale)]).convert_alpha()

    @staticmethod
    def random_int(start, end):
        n = randint(start, end)
        if n == 0:
            return 1
        return n
