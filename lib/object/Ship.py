from .GameObject import GameObject
from .Axis import Axis
from pygame import draw, Surface


class Ship(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", weapon="", health=100):
        super().__init__(x, y, size, speed, sprite)

        self.weapon = weapon
        self.health = health
        self.max_health = health
        self.last_bullet = 0
        self.initial_position = Axis(x, y)
        self.initial_sprite = sprite

    def reset(self):
        self.health = self.max_health
        self.last_bullet = 0
        self.x = self.initial_position.x
        self.y = self.initial_position.y
        self.sprite = self.initial_sprite
        self.set_size_with_sprite()

    def disable(self):
        self.sprite = Surface((0, 0))
        self.size = Axis(0, 0)

    def is_dead(self):
        return self.health <= 0

    def take_damage(self, value):
        self.health -= value

    def render(self, screen, is_player=False):
        super().render(screen)
        lifebar_size = Axis(self.size.x, self.size.y / 10)
        if is_player:
            draw.rect(screen, (255, 100, 100),
                      (self.x, self.size.y + self.y + lifebar_size.y * 2, lifebar_size.x, lifebar_size.y))
            draw.rect(screen, (100, 255, 100),
                      (self.x, self.size.y + self.y + lifebar_size.y * 2, lifebar_size.x * (self.health / 100),
                       lifebar_size.y))
            draw.rect(screen, (255, 100, 100), self.get_hitbox_rect(), border_radius=100)
        else:
            draw.rect(screen, (255, 100, 100), (self.x, self.y -
                                                lifebar_size.y * 2, lifebar_size.x, lifebar_size.y))
            draw.rect(screen, (100, 255, 100), (self.x, self.y -
                                                lifebar_size.y * 2, lifebar_size.x * (self.health / 100),
                                                lifebar_size.y))

    def get_hitbox_rect(self):
        middle = Axis(self.x + (self.size.x*0.93 / 2), self.y + (self.size.y*1.2 / 2))
        return [middle.x, middle.y, self.size.x * 0.1, self.size.x * 0.1]
