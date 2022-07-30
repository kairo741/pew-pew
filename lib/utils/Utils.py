import functools
from random import randint
import types
from pygame import transform

from lib.object.game.Axis import Axis


class Utils:

    @staticmethod
    def copy_function(f, parent_class):
        """Based on http://stackoverflow.com/a/6528148/190597 (Glenn Maynard)"""
        g = types.FunctionType(f.__code__, f.__globals__, name=f.__name__,
                            argdefs=f.__defaults__,
                            closure=f.__closure__)
        g = functools.update_wrapper(g, f)
        g.__kwdefaults__ = f.__kwdefaults__
        
        return lambda: g(parent_class)

    @staticmethod
    def copy_function2(f):
        """Based on http://stackoverflow.com/a/6528148/190597 (Glenn Maynard)"""
        g = types.FunctionType(f.__code__, f.__globals__, name=f.__name__,
                            argdefs=f.__defaults__,
                            closure=f.__closure__)
        g = functools.update_wrapper(g, f)
        g.__kwdefaults__ = f.__kwdefaults__
        
        return g


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
