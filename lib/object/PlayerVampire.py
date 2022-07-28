from pygame import Surface, transform

from lib.object.Ultimate import Ultimate
from .Player import Player


class PlayerVampire(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", level=1, sprite_ult=Surface((0, 0))):
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate, color=[13, 1, 36])
                            
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, level=level, ultimate=ultimate)
        self.sprite_ult = sprite_ult


    def enable_ultimate(self):
        super().enable_ultimate()
        self.sprite = transform.smoothscale(self.sprite_ult, self.size.to_list())

    def disable_ultimate(self):
        self.sprite = transform.smoothscale(self.initial_sprite, self.size.to_list())
        super().disable_ultimate()
        

