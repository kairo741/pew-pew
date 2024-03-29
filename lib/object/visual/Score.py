from lib.object.visual.Text import Text


class Score(Text):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", glow_scale=2, font_size=32, text=""):
        super().__init__(x, y, size, speed, sprite, glow_scale, font_size=font_size)
        self.value = 0
        self.text = text

    def add(self, value):
        self.value += value

        self.text = f'Score: {self.value}'

    def reset(self, value=0):
        self.value = 0
        return super().reset(value)