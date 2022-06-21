from turtle import width
from .GameObject import GameObject
from .Axis import Axis
from pygame import draw


class Ship(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", weapon="", health=100):
        super().__init__(x, y, size, speed, sprite)

        self.weapon = weapon
        self.health = health
        self.last_bullet = 0

    def take_damage(self, value):
        self.health -= value

    def render(self, screen, is_player=False):
        lifebar_size = Axis(self.size.x, self.size.y/10)
        if (is_player):
            draw.rect(screen, (255, 100, 100),
                      (self.x, self.size.y+self.y+lifebar_size.y*2, lifebar_size.x, lifebar_size.y))
            draw.rect(screen, (100, 255, 100),
                      (self.x*(self.health/100), self.size.y+self.y+lifebar_size.y*2, lifebar_size.x*(self.health/100), lifebar_size.y))
        else:
            draw.rect(screen, (255, 100, 100), (self.x, self.y -
                      lifebar_size.y*2, lifebar_size.x, lifebar_size.y))
            draw.rect(screen, (100, 255, 100), (self.x, self.y -
                      lifebar_size.y*2, lifebar_size.x*(self.health/100), lifebar_size.y))
        super().render(screen)
