from pygame import font


class Score:

    def __init__(self):
        self.font = font.SysFont("Consolas", 20)

    def render(self, display, score, position):
        text = self.font.render(str(round(score)), True, (255, 255, 255))
        display.blit(text, position)
