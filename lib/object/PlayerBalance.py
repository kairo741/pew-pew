from copy import deepcopy
from pygame import Surface
from .Player import Player
from .Ultimate import Ultimate

class PlayerBalance(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", ultimate=Ultimate()):
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate)

    
    def copy(self):
        copyobj = PlayerBalance()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                if type(attr) is Surface:
                    copyobj.__dict__[name] = Surface.copy(attr)
                else:
                    copyobj.__dict__[name] = deepcopy(attr)
        return copyobj