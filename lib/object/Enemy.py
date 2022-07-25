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
    ):
        super().__init__(x, y, size, speed, sprite, weapon, health, tag)
        self.next_shot = 0

    def copy(self):
        copy_obj = Enemy()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copy_obj.__dict__[name] = attr.copy()
            else:
                if type(attr) is Surface:
                    copy_obj.__dict__[name] = Surface.copy(attr)
                else:
                    copy_obj.__dict__[name] = deepcopy(attr)

        copy_obj.next_shot = copy_obj.get_random_time()
        return copy_obj

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
        life_bar_size = Axis(self.size.x, self.size.y / 10)
        health_size = life_bar_size.x * (self.health / self.max_health)
        draw.rect(screen, (255, 100, 100), (self.x, self.y - life_bar_size.y * 2, life_bar_size.x, life_bar_size.y), )
        draw.rect(screen, (100, 255, 100), (self.x, self.y - life_bar_size.y * 2, health_size, life_bar_size.y,), )
