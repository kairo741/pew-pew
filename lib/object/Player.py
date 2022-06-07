from .GameObject import GameObject
from .Axis import Axis


class Player(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", weapon="", health=100):
        super().__init__(x, y, size, speed, sprite)

        self.weapon = weapon
        self.health = health
