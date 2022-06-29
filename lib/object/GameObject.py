from pygame import Rect
from .Axis import Axis


class GameObject:
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite=""):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.sprite = sprite

    def to_rect(self):
        return Rect(self.x, self.y, self.size.x, self.size.y)

    def collided_with(self, object, rect=None):
        if rect is None:
            rect = object.to_rect()
        return self.to_rect().colliderect(rect)

    def set_size_with_sprite(self):
        self.size = Axis(self.sprite.get_width(), self.sprite.get_height())

    def get_middle(self):
        return Axis(self.x + self.size.x / 2, self.y + self.size.y / 2)

    def center(self):
        self.x -= self.size.x / 2
        self.y -= self.size.y / 2

    def render(self, screen):
        screen.blit(self.sprite, self.to_rect())
