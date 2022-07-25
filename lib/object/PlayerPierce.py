from copy import deepcopy

from lib.object.Ultimate import Ultimate
from pygame import Surface

from .Player import Player


class PlayerPierce(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout=""):
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate)

        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate)

        self.old_shoot_delay = 0

    
    def copy(self):
        copyobj = PlayerPierce()
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

    

    def enable_ultimate(self):
        self.old_shoot_delay = self.weapon.shoot_delay
        self.weapon.shoot_delay = 25

    def disable_ultimate(self):
        self.weapon.shoot_delay = self.old_shoot_delay
