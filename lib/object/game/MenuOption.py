from random import uniform
from lib.object.game.Axis import Axis
from lib.object.structure.GameObject import GameObject
from lib.object.visual.Text import Text

from pygame import transform

from lib.utils.Utils import Utils


class MenuOption(GameObject):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", glow_scale=1.6, text=None, function=lambda: None):
        super().__init__(x, y, size, speed, sprite, glow_scale, auto_set_size=True)
        self.center()
        
        self.text = text
        
        self.text.x = self.x + self.size.x/2
        self.text.y = self.y + self.size.y/2
        self.function = function

        self.normal_sprite = self.sprite.copy()
        self.rotate = 0
        self.increment = Utils.random_int(-10, 10)/10
        
        
    def render(self, screen, render_frame_time, show_hitbox=False, sprite=None):
        self.rotate += self.increment * render_frame_time
        if self.rotate > 359:
            self.rotate = 0

        self.sprite = transform.rotate(self.normal_sprite, self.rotate)
        new_size = self.sprite.get_size()
        
        offset = Axis((self.size.x + new_size[0])/2, (self.size.y + new_size[1])/2)
        offset.x -= self.size.x
        offset.y -= self.size.y
        
        super().render(screen, show_hitbox, sprite, offset=offset)
        self.text.render(screen)
    
    