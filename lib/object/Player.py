from .Axis import Axis
from .Ship import Ship
from pygame import draw


class Player(Ship):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", weapon="", health=100):
        super().__init__(x, y, size, speed, sprite, weapon, health)

    def render(self, screen):
        super().render(screen)
        lifebar_size = Axis(self.size.x, self.size.y / 10)
        draw.rect(screen, (255, 100, 100),
                  (self.x, self.size.y + self.y + lifebar_size.y * 2, lifebar_size.x, lifebar_size.y))
        draw.rect(screen, (100, 255, 100),
                  (self.x, self.size.y + self.y + lifebar_size.y * 2, lifebar_size.x * (self.health / 100),
                   lifebar_size.y))
        draw.rect(screen, (255, 100, 100), self.get_hitbox_rect(), border_radius=100)