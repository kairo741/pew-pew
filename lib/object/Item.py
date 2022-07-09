from .Axis import Axis
from .GameObject import GameObject
from random import choice


class Item(GameObject):
    def __init__(
            self,
            x=0,
            y=0,
            size=Axis.zero(),
            speed=Axis.zero(),
            sprite=""):
        super().__init__(x, y, size, speed, sprite)
        self.effect = None

    def render(self, screen):
        super().render(screen)

    def random_effect(self, player):
        effects = [player.heal, player.heal, player.heal]  # TODO - more effects
        self.effect = choice(effects)
