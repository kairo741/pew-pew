from lib.object.Axis import Axis
from lib.object.GameObject import GameObject
from lib.utils.Constants import Constants

from pygame import font

class Text(GameObject):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", glow_scale=2, font_size=20, text="", color=[255, 255, 255]):
        super().__init__(x, y, size, speed, sprite, glow_scale)

        self.font = font.Font(Constants.FONT_RETRO_GAMING, font_size)
        self.text = text
        self.color = color
        

    def set_text(self, txt):
        self.text = txt

    def add(self, n):
        try:
            int(self.text)
        except:
            self.text = "0"
        self.text = str(int(self.text)+n)

    def reset(self, value=0):
        self.text = str(value)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def render(self, screen, align="center"):
        text = self.font.render(str(self.text), True, self.color)
        size = text.get_size()
        if align == "center":
            screen.blit(text, [self.x-size[0]/2, self.y-size[1]/2])

        elif align == "top-left":
            screen.blit(text, [self.x, self.y])

        elif align == "top-right":
            screen.blit(text, [self.x-size[0], self.y])

