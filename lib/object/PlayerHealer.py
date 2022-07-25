from .Player import Player

class PlayerHealer(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout=""):
        super().__init__(x, y, size, speed, sprite, weapon, health, layout)

    def player_passive(self, render_frame_time):
        if self.max_health > self.health > 0:
            self.health += (self.max_health * 0.0003) * render_frame_time