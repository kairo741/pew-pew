from lib.object.players.Player import Player

from lib.utils.Constants import Constants
from .Bullet import Bullet


class BulletHeal(Bullet):

    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", damage=10, tag=Constants.TAG_PLAYER,
                 source_reference=None, crit_rate=0):
        super().__init__(x, y, size, speed, sprite, damage, tag, source_reference, crit_rate)

    def hit_callback(self, object_hit, collision):
        if not isinstance(object_hit, Player):
            super().hit_callback(object_hit, collision)
            
        if object_hit.tag == Constants.TAG_PLAYER:
            heal_amount = self.source_reference.max_health * 0.1

            if (object_hit.health + heal_amount) < object_hit.max_health:
                object_hit.health += heal_amount
                
                self.source_reference.add_xp(heal_amount * 5)
            else:
                object_hit.health = object_hit.max_health