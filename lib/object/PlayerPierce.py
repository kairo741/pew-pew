from lib.object.Ultimate import Ultimate

from .Player import Player


class PlayerPierce(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout=""):
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate)

        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate)

        self.old_shoot_delay = 0


    def enable_ultimate(self):
        self.old_shoot_delay = self.weapon.shoot_delay
        self.weapon.shoot_delay = 25

    def disable_ultimate(self):
        self.weapon.shoot_delay = self.old_shoot_delay
