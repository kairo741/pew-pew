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
