from pygame import draw, time
from utils.Constants import Constants
from utils.Presets import Presets

from .Axis import Axis
from .Ship import Ship


class Player(Ship):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", weapon="", health=100, layout=Presets.PRIMARY_KB_LAYOUT):
        super().__init__(x, y, size, speed, sprite, weapon, health)
        self.layout = layout

    def take_damage(self, value):
        super().take_damage(value)
        if not self.is_alive():
            self.disable()

    def control_ship(self, keys, render_frame_time, limit):
        if self.is_alive():
            if keys[self.layout.right]:
                if self.x + self.size.x < limit.x:
                    self.x += self.speed.x * render_frame_time

            if keys[self.layout.left]:
                if self.x > 2:
                    self.x -= self.speed.x * render_frame_time

            if keys[self.layout.up]:
                if self.y > 2:
                    self.y -= self.speed.y * render_frame_time

            if keys[self.layout.down]:
                if self.y + self.size.y < limit.y:
                    self.y += self.speed.y * render_frame_time


    def control_shoot(self, keys, bullet_manager):
        if self.is_alive():
            if keys[self.layout.shoot]:
                if time.get_ticks() - self.last_bullet > self.weapon.shoot_delay:
                    for generated_bullet in self.weapon.make_bullets(self.get_middle()):
                        bullet_manager.shoot(generated_bullet)

                    Constants.SFX_LASER.play()
                    self.last_bullet = time.get_ticks()

    def control_ultimate(self, keys, *conditions, action):
        if self.is_alive():
            if keys[self.layout.ultimate]:
                if all(conditions):
                    action()


    def render(self, screen):
        super().render(screen)
        lifebar_size = Axis(self.size.x, self.size.y / 10)
        draw.rect(screen, (255, 100, 100),
                  (self.x, self.size.y + self.y + lifebar_size.y * 2, lifebar_size.x, lifebar_size.y))
        draw.rect(screen, (100, 255, 100),
                  (self.x, self.size.y + self.y + lifebar_size.y * 2, lifebar_size.x * (self.health / 100),
                   lifebar_size.y))
        draw.rect(screen, (75, 255, 75), self.get_hitbox_rect(), border_radius=100)
