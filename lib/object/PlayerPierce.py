from lib.object.Ultimate import Ultimate

from .Player import Player


class PlayerPierce(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", level=1):
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate, color=[43, 71, 79])

        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level=level)

        self.old_shoot_delay = 0
        self.old_damage = 0

    
    def save_attributes(self):
        self.old_shoot_delay = self.weapon.shoot_delay
        self.old_damage = self.weapon.bullet.damage

    def restore_attributes(self):
        self.weapon.shoot_delay = self.old_shoot_delay
        self.weapon.bullet.damage = self.old_damage

    def enable_ultimate(self):
        self.save_attributes()

        self.weapon.shoot_delay = 25
        self.weapon.bullet.damage *= 1.75

    def disable_ultimate(self):
        self.restore_attributes()
