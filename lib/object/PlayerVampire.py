from .Player import Player


class PlayerVampire(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", level=1):
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, level=level)
