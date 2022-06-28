from pygame import Rect
from .Axis import Axis


class GameObject:
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite=""):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.sprite = sprite

    def toRect(self):
        return Rect(self.x, self.y, self.size.x, self.size.y)

    def collided_with(self, object):
        return self.toRect().colliderect(object.toRect())

    def setSizeWithSprite(self):
        self.size = Axis(self.sprite.get_width(), self.sprite.get_height())
        
    def getMiddle(self):
        return Axis(self.x+self.size.x/2, self.y+self.size.y/2)
    
    def center(self):
        self.x -= self.size.x/2
        self.y -= self.size.y/2

    def render(self, screen):
        screen.blit(self.sprite, self.toRect())

