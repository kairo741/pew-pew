from copy import deepcopy
from pygame import Surface

from lib.object.Ultimate import Ultimate
from .Player import Player


class PlayerHealer(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout=""):
        super().__init__(x, y, size, speed, sprite, weapon, health, layout)

    def player_passive(self, render_frame_time):
        if self.max_health > self.health > 0:
            self.health += (self.max_health * 0.0003) * render_frame_time

    
    def copy(self):
        copyobj = PlayerHealer()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                if type(attr) is Ultimate:
                    copyobj.__dict__[name] = attr.copy(parent=copyobj)
                else:    
                    copyobj.__dict__[name] = attr.copy()
            else:
                if type(attr) is Surface:
                    copyobj.__dict__[name] = Surface.copy(attr)
                else:
                    copyobj.__dict__[name] = deepcopy(attr)
        return copyobj
