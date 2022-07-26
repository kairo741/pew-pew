from .Player import Player
from .Ultimate import Ultimate


class PlayerBalance(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", ultimate=Ultimate(), level=1):
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level=level)
