from .GameObject import GameObject
from .Axis import Axis
from lib.utils.Constants import Constants
from pygame import Surface, transform


class Ship(GameObject):
    def __init__(
            self,
            x=0,
            y=0,
            size=Axis.zero(),
            speed=Axis.zero(),
            sprite="",
            weapon="",
            health=100,
            tag=Constants.TAG_PLAYER
    ):
        super().__init__(x, y, size, speed, sprite)

        self.weapon = weapon
        self.health = health
        self.max_health = health
        self.last_bullet = 0
        self.initial_position = Axis(x, y)
        self.initial_sprite = sprite
        self.tag = tag

    def reset(self):
        self.x = self.initial_position.x
        self.y = self.initial_position.y
        self.revive()

    def disable(self):
        self.sprite = Surface((0, 0))
        self.size = Axis(0, 0)

    def revive(self):
        self.health = self.max_health
        self.last_bullet = 0
        self.sprite = self.initial_sprite.copy()
        self.set_size_with_sprite(set_glow=False)

    def set_size_with_sprite(self, set_glow=True):
        self.initial_sprite = self.sprite.copy()
        return super().set_size_with_sprite(set_glow)

    def is_alive(self):
        return self.health > 0

    def take_damage(self, value):
        self.health -= value
