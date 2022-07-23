from copy import deepcopy
from pygame import Surface
from .Player import Player

class PlayerHealer(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout=""):
        super().__init__(x, y, size, speed, sprite, weapon, health, layout)

    def render(self, screen):
        if self.health < self.max_health:
            self.health+=self.max_health*0.00003
        return super().render(screen)

    def copy(self):
        copyobj = PlayerHealer()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                if type(attr) is Surface:
                    copyobj.__dict__[name] = Surface.copy(attr)
                else:
                    copyobj.__dict__[name] = deepcopy(attr)
        return copyobj