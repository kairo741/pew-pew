from lib.object.players.Player import Player
from lib.object.game.Ultimate import Ultimate
from lib.utils.Constants import Constants
from pygame.mixer import Channel


class PlayerBalance(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", ultimate=Ultimate(), level=1, time_stop= lambda: None):
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate)
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level=level)

        self.time_stop = time_stop

    def enable_ultimate(self):
        super().enable_ultimate()
        channel = Channel(Constants.MIXER_CHANNEL_EFFECTS)
        channel.play(Constants.SFX_TIME_STOP)
        self.time_stop(True)

    def disable_ultimate(self):
        self.time_stop(False)
        super().disable_ultimate()
