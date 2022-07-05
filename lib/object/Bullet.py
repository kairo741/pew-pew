from utils.Constants import Constants
from .GameObject import GameObject
from .Axis import Axis


class Bullet(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", damage=10, pierce=False, tag=Constants.TAG_PLAYER):
        super().__init__(x, y, size, speed, sprite)
        self.pierce = pierce
        self.damage = damage
        self.tag = tag



