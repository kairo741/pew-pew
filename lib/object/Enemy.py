from copy import deepcopy
from random import randint

from pygame import Surface, draw, time, mixer

from lib.utils.Constants import Constants
from .Axis import Axis
from .Ship import Ship


class Enemy(Ship):
    def __init__(
            self,
            x=0,
            y=0,
            size=Axis.zero(),
            speed=Axis.zero(),
            sprite="",
            weapon="",
            health=100,
            tag=Constants.TAG_ENEMY,
            level=1
    ):
        super().__init__(x, y, size, speed, sprite, weapon, health, tag, level=level)
        self.next_shot = 0
        self.glow_scale = 2.5
        self.glow_color = [255, 30, 30]

    def get_random_time(self):
        if self.weapon is not None:
            return time.get_ticks() + randint(self.weapon.shoot_delay, self.weapon.shoot_delay * 2)

    def shoot(self, bullet_manager):
        if self.weapon is not None:
            if time.get_ticks() > self.next_shot:
                bullets = self.weapon.make_bullets(Axis(self.get_middle().x, self.y + self.size.y), self.size)
                for generated_bullet in bullets:
                    bullet_manager.shoot(generated_bullet)
                channel = mixer.Channel(Constants.SFX_MIXER_CHANNEL)
                channel.play(Constants.SFX_LASER_2)
                self.next_shot = self.get_random_time()


    def render(self, screen):
        super().render(screen)
        self.render_level(screen, align="top")
        self.render_lifebar(screen, align="top")
