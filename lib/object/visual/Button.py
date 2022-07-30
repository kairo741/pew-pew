from lib.object.game.Axis import Axis
from lib.object.structure.GameObject import GameObject

from pygame import Surface, draw

class Button(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", glow_scale=2, on_click=lambda: None, content=Surface((0, 0))):
        super().__init__(x, y, size, speed, sprite, glow_scale)

        self.on_click = on_click
        self.cursor_pos = [0, 0]
        self.cursor_clicked = 0
        self.color = (255, 255, 255)
        self.content = content
        self.width = 1

    def check_collision(self):
        if self.to_rect().collidepoint(self.cursor_pos[0], self.cursor_pos[1]):
            self.width = 0
            if self.cursor_clicked:
                self.on_click()
        else:
            self.width = 1
    

    def render(self, screen, show_hitbox=False):
        self.check_collision()
        draw.rect(screen, self.color, self.to_rect(), self.width)
        size_content = self.content.get_size()
        pos_content = Axis(self.x+size_content[0]/4, self.y+size_content[1]/4)
        screen.blit(self.content, pos_content.to_list())