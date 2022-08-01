from lib.object.game.Axis import Axis
from lib.object.game.Ultimate import Ultimate
from lib.object.players.Player import Player
from pygame import Surface, transform


class PlayerSpeed(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", level=1):
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate, duration=8, color=[23, 0, 0])
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level=level)
        self.rotate = 0
        self.old_sprite = Surface((0, 0))
        self.old_speed = Axis(0, 0)
        self.old_shoot_delay = None

    def save_attributes(self):
        self.old_sprite = self.sprite
        self.old_speed = self.speed
        self.old_shoot_delay = self.weapon.shoot_delay

    def restore_attributes(self):
        self.sprite = self.old_sprite
        self.speed = self.old_speed
        self.weapon.shoot_delay = self.old_shoot_delay

    def enable_ultimate(self):
        super().enable_ultimate()
        self.save_attributes()
        self.weapon.shoot_delay = 10**10
        self.speed = self.speed.scale_to(2)
        self.rotate = 1
        self.is_invincible = True

    def disable_ultimate(self):
        self.restore_attributes()
        self.rotate = 0
        self.is_invincible = False
        super().disable_ultimate()

    def render(self, screen, render_frame_time):
        if self.rotate != 0:
            self.sprite = transform.rotate(self.old_sprite, self.rotate)
            self.sprite = transform.scale(self.sprite, self.size.to_list())

            self.rotate -= 10
            if self.rotate < -359:
                self.rotate = 1

        return super().render(screen, render_frame_time)
