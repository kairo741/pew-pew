from pygame import Rect
from object.Size import Size

class GameObject:


    def __init__(self, x, y, size=Size(0, 0), sprite=""):
        self.x = x
        self.y = y
        self.size = size
        self.sprite = sprite

    def toRect(self):
        return Rect(self.x, self.y, self.size.x, self.size.y)

    def setSizeWithSprite(self):
        self.size = Size(self.sprite.get_width(), self.sprite.get_height())
        
    def getMiddle(self):
        return Size(self.x+self.size.x/2, self.y+self.size.y/2)
