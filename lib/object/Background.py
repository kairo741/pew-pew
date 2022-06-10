from .GameObject import GameObject
from .Axis import Axis


class Background(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite=""):
        super().__init__(x, y, size, speed, sprite)

    # def render(self, screen):


