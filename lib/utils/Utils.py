from random import randint
from pygame import transform, display

from lib.object.Axis import Axis


class Utils:
    @staticmethod
    def scale_image(image, scale):
        horizontal_size = display.get_window_size()[0]*0.00067
        img_size = Axis(image.get_width(), image.get_height())

        return transform.smoothscale(image, [(img_size.x * scale)*horizontal_size, (img_size.y * scale)*horizontal_size])

    @staticmethod
    def random_int(start, end):
        n = randint(start, end)
        if (n == 0):
            return 1
        return n
