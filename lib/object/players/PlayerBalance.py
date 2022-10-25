from lib.object.players.Player import Player
from lib.object.game.Ultimate import Ultimate
from lib.utils.Constants import Constants
from pygame.mixer import Channel


class PlayerBalance(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", ultimate=Ultimate(), level=1, time_stop= lambda: None):
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate)
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level=level)

        self.time_stop = time_stop
        self.bounce_times = 1

        self.base_sprite = ""

    def enable_ultimate(self):
        super().enable_ultimate()
        channel = Channel(Constants.MIXER_CHANNEL_ULT)
        channel.play(Constants.SFX_TIME_STOP)

        self.bounce_times = self.bounce_times * 10
        self.time_stop(True)
        self.base_sprite = self.weapon.bullet.sprite.copy()
        self.weapon.bullet.sprite = self.weapon.bullet.super_sprite

    def disable_ultimate(self):
        self.bounce_times = int(self.level/5)+1
        self.time_stop(False)
        self.weapon.bullet.sprite = self.base_sprite.copy()
        super().disable_ultimate()

    def set_level(self, level):
        super().set_level(level)
        self.bounce_times = int(self.level/5)+1
