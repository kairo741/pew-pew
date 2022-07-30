from lib.object.game.Ultimate import Ultimate
from lib.object.players.Player import Player

class PlayerBerserk(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", ultimate=Ultimate(), level=1):

        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate, duration=1, color=[20, 0, 23])
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level)

    def player_passive(self, render_frame_time):
        if self.health > 1:
            self.health -= (self.health * 0.0003)*render_frame_time
        return super().player_passive(render_frame_time)

    def shoot(self, bullet_manager, damage_multiplier=1):
        damage_multiplier = (1+1-(self.health / self.max_health))**4
        shoot_delay_multiplier = self.health / self.max_health
        if shoot_delay_multiplier < 0.3:
            shoot_delay_multiplier = 0.3

        return super().shoot(bullet_manager, damage_multiplier, shoot_delay_multiplier)

    def enable_ultimate(self):
        super().enable_ultimate()
        self.health = 1
