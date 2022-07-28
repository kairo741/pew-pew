from lib.utils.Constants import Constants
from .Bullet import Bullet
from .Axis import Axis


class BulletVamp(Bullet):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", damage=10, tag=Constants.TAG_PLAYER,
                 source_reference=None):
        super().__init__(x, y, size, speed, sprite, damage, tag, source_reference)

    def hit_callback(self, object, collision):
        super().hit_callback(object, collision)
        if self.source_reference.health < self.source_reference.max_health:
            self.source_reference.health += self.source_reference.max_health * 0.02

