from copy import deepcopy
from pygame import Surface
from lib.utils.Constants import Constants
from .Bullet import Bullet


class BulletBounce(Bullet):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", damage=10, tag=Constants.TAG_PLAYER,
                 source_reference=None):
        super().__init__(x, y, size, speed, sprite, damage, tag, source_reference)

    def copy(self):
        copy_obj = BulletBounce()
        for name, attr in self.__dict__.items():
            if type(attr) is Surface:
                copy_obj.__dict__[name] = Surface.copy(attr)
            else:
                copy_obj.__dict__[name] = deepcopy(attr)
        return copy_obj
