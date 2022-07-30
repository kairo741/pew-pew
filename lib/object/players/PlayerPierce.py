from pygame import Surface, transform
from lib.object.game.Ultimate import Ultimate
from lib.object.players.Player import Player


class PlayerPierce(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", level=1, sprite_ult=Surface((0, 0))):
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate, color=[0, 16, 23], shake_duration=None)

        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level=level)

        self.old_shoot_delay = 0
        self.old_damage = 0
        self.sprite_ult = sprite_ult

    
    def save_attributes(self):
        self.old_shoot_delay = self.weapon.shoot_delay
        self.old_damage = self.weapon.bullet.damage

    def restore_attributes(self):
        self.weapon.shoot_delay = self.old_shoot_delay
        self.weapon.bullet.damage = self.old_damage

        self.sprite = transform.smoothscale(self.initial_sprite, self.size.to_list())

    def enable_ultimate(self):
        super().enable_ultimate()
        self.save_attributes()

        self.sprite = transform.smoothscale(self.sprite_ult, self.size.to_list())
        self.weapon.shoot_delay = 25
        self.weapon.bullet.damage *= 1.75

    def disable_ultimate(self):
        self.restore_attributes()
        super().disable_ultimate()
