from .Axis import Axis
from .GameObject import GameObject


class Item(GameObject):
    def __init__(
            self,
            x=0,
            y=0,
            size=Axis.zero(),
            speed=Axis.zero(),
            sprite=""):
        super().__init__(x, y, size, speed, sprite)

    def render(self, screen):
        super().render(screen)
