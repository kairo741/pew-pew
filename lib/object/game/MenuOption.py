from lib.object.structure.GameObject import GameObject
from lib.object.visual.Text import Text


class MenuOption(GameObject):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", glow_scale=2, text=None):
        super().__init__(x, y, size, speed, sprite, glow_scale)
        
        self.text = text
        
        self.text.x = x
        self.text.y = y
        
        
    def render(self, screen, show_hitbox=False, sprite=None):
        super().render(screen, show_hitbox, sprite)
        self.text.render(screen)
    
    