from lib.object.Axis import Axis
from lib.object.Ultimate import Ultimate
from .Player import Player

from pygame import draw

class PlayerCharge(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", ultimate=Ultimate(), level=1):
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level)

        self.charge_time = 0

    def player_passive(self, render_frame_time):
        self.charge_time += (1) * render_frame_time
        return super().player_passive(render_frame_time)

    def shoot(self, bullet_manager):
        charge = (self.charge_time/100)
        self.charge_time = 0

        if charge > 2:
            charge = 2

        elif charge < 1:
            charge=1
        return super().shoot(bullet_manager, damage_multiplier=charge**6)

    def render_charge_shot(self, screen):
        bar_size = Axis(self.size.x, self.size.y / 10)
        multiplier = (self.charge_time / 100) / 2
        if multiplier > 1:
            multiplier = 1

        char_size = multiplier * bar_size.x

        draw.rect(screen, (255 * multiplier, 100, 100), (self.x, self.y + self.size.y + bar_size.y * 6, char_size, bar_size.y))

    def render(self, screen, render_frame_time):
        self.render_charge_shot(screen)
        return super().render(screen, render_frame_time)