from copy import deepcopy

from pygame import Surface
from lib.object.Player import Player
from lib.utils.Constants import Constants
from .GameObject import GameObject
from .Axis import Axis


class Bullet(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", damage=10, tag=Constants.TAG_PLAYER, source_reference=None):
        super().__init__(x, y, size, speed, sprite)
        self.damage = damage
        self.tag = tag
        self.source_reference = source_reference
        self.glow_scale = 2.1
        

    def hit_callback(self, object_hit, collision):
        if isinstance(self.source_reference, Player):
            self.source_reference.damage_dealt+=self.damage