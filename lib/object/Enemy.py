from random import randint

from pygame import draw, time
from utils.Constants import Constants

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
        self.next_shot = self.get_random_time()

    def get_random_time(self):
        return time.get_ticks()+randint(self.weapon.shoot_delay, self.weapon.shoot_delay*2)

    def shoot(self, bullet_manager):
        if time.get_ticks() > self.next_shot:
            bullets = self.weapon.make_bullets(Axis(self.get_middle().x, self.y + self.size.y))
            for generated_bullet in bullets:
                bullet_manager.shoot(generated_bullet)

            Constants.SFX_LASER_2.play()
            self.next_shot = self.get_random_time()

    def render(self, screen):
        super().render(screen)
        lifebar_size = Axis(self.size.x, self.size.y / 10)
        draw.rect(
            screen,
            (255, 100, 100),
            (self.x, self.y - lifebar_size.y * 2, lifebar_size.x, lifebar_size.y),
        )
        draw.rect(
            screen,
            (100, 255, 100),
            (
                self.x,
                self.y - lifebar_size.y * 2,
                lifebar_size.x * (self.health / 100),
                lifebar_size.y,
            ),
        )
