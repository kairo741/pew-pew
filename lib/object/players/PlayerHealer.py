from lib.object.players.Player import Player
from lib.object.game.Ultimate import Ultimate
from pygame import Surface, transform


class PlayerHealer(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", team=None, level=1,
                 sprite_ult=Surface((0, 0))):
        self.team = team
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate, duration=7,
                            color=[23, 23, 0])
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level=level)
        self.sprite_ult = sprite_ult

    def player_passive(self, render_frame_time):
        if self.max_health > self.health > 0:
            self.health += (self.max_health * 0.0003) * render_frame_time

    def enable_ultimate(self):
        super().enable_ultimate()
        self.sprite = transform.smoothscale(self.sprite_ult, self.size.to_list())
        for player in self.team:
            if not player.is_alive():
                player.revive()

            player.health = player.max_health
            player.is_invincible = True

    def disable_ultimate(self):
        for player in self.team:
            player.is_invincible = False
        self.sprite = transform.smoothscale(self.initial_sprite, self.size.to_list())
        super().disable_ultimate()
