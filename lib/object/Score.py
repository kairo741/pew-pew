from pygame import font


class Score:
    def __init__(self):
        self.font = font.SysFont("Consolas", 34)
        self.value = 0

    def reset(self):
        self.value = 0

    def add(self, value):
        self.value+=value

    def render(self, display, position):
        text = self.font.render(str(round(self.value)), True, (255, 255, 255))
        display.blit(text, position.to_list())
    


