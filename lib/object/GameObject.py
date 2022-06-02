from pygame import Rect

class GameObject:

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def toRect(self):
        return Rect(self.x, self.y, self.size.x, self.size.y)
