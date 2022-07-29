from pygame import font
from lib.utils.Constants import Constants
from lib.object.Text import Text


class Score(Text):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", glow_scale=2, font_size=20, text=""):
        super().__init__(x, y, size, speed, sprite, glow_scale)
        self.value = 0
        self.text = text

    def add(self, value):
        self.value += value

        self.text = f'Score: {self.value}'
