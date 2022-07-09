from pygame import font

from utils.Constants import Constants


class Number:
    def __init__(self, x, y, text, start_time, duration, color, size, opacity=255):
        self.font = font.Font(Constants.FONT_NUMBER, size)

        self.x = x
        self.y = y
        self.text = text
        self.color = color

        self.start_time = start_time        
        self.duration = duration
        self.opacity = opacity


    def render(self, display):
        text = self.font.render(str(round(self.text)), True, self.color)
        text.set_alpha(self.opacity)
        display.blit(text, (self.x, self.y))
