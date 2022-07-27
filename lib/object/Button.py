from lib.object.Axis import Axis
from lib.object.GameObject import GameObject

from pygame import Surface, draw

class Button(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", glow_scale=2, on_click=lambda: None, content=Surface((0, 0))):
        super().__init__(x, y, size, speed, sprite, glow_scale)

        self.on_click = on_click
        self.cursor_pos = [0, 0]
        self.cursor_clicked = 0
        self.color = (255, 255, 255)
        self.content = content


    def check_collision(self):
        if self.to_rect().collidepoint(self.cursor_pos[0], self.cursor_pos[1]):
            self.color = (100, 255, 100)
            if self.cursor_clicked:
                self.color = (255, 100, 100)
                self.on_click()
        else:
            self.color = (255, 255, 255)

    

    def render(self, screen, show_hitbox=False):
        self.check_collision()
        draw.rect(screen, self.color, self.to_rect())
        screen.blit(self.content, self.to_rect())