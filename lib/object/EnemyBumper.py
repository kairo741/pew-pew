from copy import deepcopy

from pygame import Surface

from lib.object.Enemy import Enemy
from lib.utils.Constants import Constants
from .Axis import Axis


class EnemyBumper(Enemy):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", weapon="", health=100,
                 tag=Constants.TAG_ENEMY, level=1):
        super().__init__(x, y, size, speed, sprite, weapon, health, tag, level=level)

    def enemy_passive(self, screen_size):
        if self.y < -self.size.y:
            self.speed.y = -self.speed.y
        elif self.x < -self.size.x:
            self.speed.x = -self.speed.x
        elif self.x > screen_size.x:
            self.speed.x = -self.speed.x
        elif self.y > screen_size.y:
            self.speed.y = -self.speed.y
