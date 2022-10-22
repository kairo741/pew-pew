from pygame import draw

from lib.object.visual.Text import Text


class Bar:
    def __init__(self, x, y, value=0, max_value=1, bar_width=0, title=""):
        self.x = x
        self.y = y
        self.value = value
        self.max_value = max_value
        self.bar_width = bar_width
        self.title = Text(x-self.bar_width*0.2, y=y, text=title, font_size=28)

    def render(self, screen):
        self.title.render(screen, align="right")
        color = [255, 20, 20]
        color[1] += int(235 * (1-(self.value/self.max_value)))
        
        draw.rect(screen, color, (self.x, self.y, self.bar_width*(self.value/self.max_value), self.bar_width*0.25), border_radius=5)
        draw.rect(screen, (255, 255, 255), (self.x, self.y, self.bar_width, self.bar_width*0.25), width=2, border_radius=5)