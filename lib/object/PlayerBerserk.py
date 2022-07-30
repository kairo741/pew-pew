from lib.object.Ultimate import Ultimate
from .Player import Player

class PlayerBerserk(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", ultimate=Ultimate(), level=1):

        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate, duration=1, color=[20, 0, 23])
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level)

    def shoot(self, bullet_manager, damage_multiplier=1):
        damage_multiplier = (1+1-(self.health / self.max_health))**5
        return super().shoot(bullet_manager, damage_multiplier)

    def enable_ultimate(self):
        super().enable_ultimate()
        self.health = 1
