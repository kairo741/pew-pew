from .Player import Player
from .Ultimate import Ultimate


class PlayerHealer(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", team=None, level=1):
        self.team = team
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate, duration=6, color=[23, 23, 0])
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level=level)

    def player_passive(self, render_frame_time):
        if self.max_health > self.health > 0:
            self.health += (self.max_health * 0.0003) * render_frame_time

    def enable_ultimate(self):
        super().enable_ultimate()
        for player in self.team:
            if not player.is_alive():
                player.revive()

            player.health = player.max_health
            player.is_invincible = True

    def disable_ultimate(self):
        for player in self.team:
            player.is_invincible = False

        super().disable_ultimate()
