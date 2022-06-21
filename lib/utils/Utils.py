from random import randint
from pygame import transform


class Utils:
    @staticmethod
    def scale_image(image, scale):
        return transform.smoothscale(image, (image.get_width() * scale, image.get_height() * scale))

    @staticmethod
    def random_int(start, end):
        n = randint(start, end)
        if (n == 0):
            return 1
        return n
