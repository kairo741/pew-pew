from random import randint, uniform
from lib.object.Player import Player
from lib.utils.Constants import Constants
from .Axis import Axis
from .GameObject import GameObject


class Bullet(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", damage=10, tag=Constants.TAG_PLAYER,
                 source_reference=None):
        super().__init__(x, y, size, speed, sprite)
        self.damage = damage
        self.tag = tag
        self.source_reference = source_reference
        self.glow_scale = 0

        self.crit_rate = 0.25
        if uniform(0, 1) < self.crit_rate:
            self.damage *=2

    def hit_callback(self, object_hit, collision):
        if isinstance(self.source_reference, Player):
            if self.damage < object_hit.health:
                self.source_reference.xp += self.damage
            else:
                self.source_reference.xp += object_hit.health
