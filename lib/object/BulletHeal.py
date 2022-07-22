from copy import deepcopy
from pygame import Surface
from lib.utils.Constants import Constants
from .Bullet import Bullet

class BulletHeal(Bullet):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", damage=10, tag=Constants.TAG_PLAYER, source_reference=None):
        super().__init__(x, y, size, speed, sprite, damage, tag, source_reference)

    
    def hit_callback(self, object):
        if self.source_reference.health < self.source_reference.max_health:
            self.source_reference.health += self.source_reference.max_health*0.02

    def copy(self):
        copyobj = BulletHeal()
        for name, attr in self.__dict__.items():
            if type(attr) is Surface:
                copyobj.__dict__[name] = Surface.copy(attr)
            else:
                copyobj.__dict__[name] = deepcopy(attr)
        return copyobj