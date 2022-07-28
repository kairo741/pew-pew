from .Player import Player
from .Ultimate import Ultimate


class PlayerBalance(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", ultimate=Ultimate(), level=1, time_stop= lambda: None):
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate)
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level=level)

        self.time_stop = time_stop

    def enable_ultimate(self):
        super().enable_ultimate()
        self.time_stop(True)

    def disable_ultimate(self):
        self.time_stop(False)
        super().disable_ultimate()
