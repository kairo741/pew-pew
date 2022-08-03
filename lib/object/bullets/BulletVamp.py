from lib.object.game.Axis import Axis
from lib.utils.Constants import Constants
from .Bullet import Bullet


class BulletVamp(Bullet):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", damage=10, tag=Constants.TAG_PLAYER,
                 source_reference=None, crit_rate=0):
        super().__init__(x, y, size, speed, sprite, damage, tag, source_reference, crit_rate)

    def hit_callback(self, object, collision):
        super().hit_callback(object, collision)
        if 0 < self.source_reference.health < self.source_reference.max_health:
            self.source_reference.health += self.source_reference.max_health * 0.02
