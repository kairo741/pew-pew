from copy import deepcopy

from pygame import Surface
from lib.utils.Constants import Constants
from .GameObject import GameObject
from .Axis import Axis


class Bullet(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", damage=10, tag=Constants.TAG_PLAYER):
        super().__init__(x, y, size, speed, sprite)
        self.damage = damage
        self.tag = tag


    def copy(self):
        copyobj = Bullet()
        for name, attr in self.__dict__.items():
            if type(attr) is Surface:
                copyobj.__dict__[name] = Surface.copy(attr)
            else:
                copyobj.__dict__[name] = deepcopy(attr)
        return copyobj