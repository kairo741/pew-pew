from pygame import font
from lib.utils.Constants import Constants


class Score:
    def __init__(self):
        # self.font = font.SysFont("Consolas", 34)
        self.font = font.Font(Constants.FONT_RETRO_GAMING, 20)
        self.value = 0

    def reset(self):
        self.value = 0

    def add(self, value):
        self.value += value

    def render(self, display, position):
        text = self.font.render(f'Score: {str(round(self.value))}', True, (255, 255, 255))
        display.blit(text, position.to_list())
