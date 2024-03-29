from random import uniform
from lib.object.players.Player import Player
from lib.utils.Constants import Constants
from lib.object.game.Axis import Axis
from lib.object.structure.GameObject import GameObject


class Bullet(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", damage=10, tag=Constants.TAG_PLAYER,
                 source_reference=None, crit_rate=0):
        super().__init__(x, y, size, speed, sprite)
        self.damage = damage
        self.tag = tag
        self.source_reference = source_reference
        self.glow_scale = 0

        self.is_crit = False
        self.crit_rate = crit_rate
        if uniform(0, 1) < self.crit_rate:
            self.damage *=1.5
            self.is_crit = True

    def shoot_callback(self):
        pass

    def hit_callback(self, object_hit, collision):
        if isinstance(self.source_reference, Player):
            if self.source_reference.level - object_hit.level < 4:

                if self.damage < object_hit.health:
                    self.source_reference.add_xp(self.damage)
                else:
                    self.source_reference.add_xp(object_hit.health)

                self.source_reference.add_xp(object_hit.level * 10)
