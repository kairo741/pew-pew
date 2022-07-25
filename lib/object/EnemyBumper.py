from copy import deepcopy

from pygame import Surface

from lib.object.Enemy import Enemy
from lib.utils.Constants import Constants
from .Axis import Axis


class EnemyBumper(Enemy):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", weapon="", health=100,
                 tag=Constants.TAG_ENEMY):
        super().__init__(x, y, size, speed, sprite, weapon, health, tag)

    def enemy_passive(self, screen_size):
        if self.y < -self.size.y:
            self.speed.y = -self.speed.y
        elif self.x < -self.size.x:
            self.speed.x = -self.speed.x
        elif self.x > screen_size.x:
            self.speed.x = -self.speed.x
        elif self.y > screen_size.y:
            self.speed.y = -self.speed.y

    def copy(self):
        copy_obj = EnemyBumper()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copy_obj.__dict__[name] = attr.copy()
            else:
                if type(attr) is Surface:
                    copy_obj.__dict__[name] = Surface.copy(attr)
                else:
                    copy_obj.__dict__[name] = deepcopy(attr)

        copy_obj.next_shot = copy_obj.get_random_time()
        return copy_obj
