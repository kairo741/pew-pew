from lib.object.Axis import Axis
from lib.object.Ultimate import Ultimate
from .Player import Player

from pygame import Surface, draw, transform

class PlayerCharge(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", ultimate=Ultimate(), level=1, sprite_mid=Surface((0, 0)), sprite_full=Surface((0, 0))):
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate,
                            color=[20, 0, 23])
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level)
        self.sprite_mid = sprite_mid
        self.sprite_full = sprite_full

        self.charge_time = 0

        self.cancel_charge_time = False

    def enable_ultimate(self):
        super().enable_ultimate()
        self.cancel_charge_time = True

    def disable_ultimate(self):
        self.cancel_charge_time = False
        super().disable_ultimate()


    def get_charge(self, raw=False):
        charge = (self.charge_time/100)

        if self.cancel_charge_time:
            return 2

        if raw:
            return charge
        
        if charge > 2:
            charge = 2

        elif charge < 1:
            charge = 1

        return charge

    def check_sprite_change(self):
        charge = self.get_charge()
        if charge == 2 and self.sprite != self.sprite_full:
            self.sprite = transform.smoothscale(self.sprite_full.copy(), self.size.to_list())

        elif charge > 1 and self.sprite != self.sprite_mid:
            self.sprite = transform.smoothscale(self.sprite_mid.copy(), self.size.to_list())

        elif self.sprite != self.initial_sprite:
            self.sprite = transform.smoothscale(self.initial_sprite.copy(), self.size.to_list())


    def player_passive(self, render_frame_time):
        charge_increment = (1+(1/self.weapon.shoot_delay)*100)
        self.charge_time += charge_increment * render_frame_time

        self.check_sprite_change()
        return super().player_passive(render_frame_time)


    def shoot(self, bullet_manager):
        charge = self.get_charge()
        self.charge_time = 0

        return super().shoot(bullet_manager, damage_multiplier=charge**4.5)

    def render_charge_shot(self, screen):
        bar_size = Axis(self.size.x, self.size.y / 10)
        multiplier = self.get_charge(raw=True) / 2
        if multiplier > 1:
            multiplier = 1

        char_size = multiplier * bar_size.x

        draw.rect(screen, (255, 255, 255), (self.x, self.y + self.size.y + bar_size.y * 6, char_size, bar_size.y))

    def render_level(self, screen, align="bottom"):
        return super().render_level(screen, align, 1.8)

    def render(self, screen, render_frame_time):
        self.render_charge_shot(screen)
        return super().render(screen, render_frame_time)