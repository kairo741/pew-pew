from pygame import Rect, transform
from .Axis import Axis
from lib.utils.Constants import Constants


class GameObject:
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite=""):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.sprite = sprite
        self.glow = Constants.SPRITE_GLOW.convert_alpha()

    def to_rect(self):
        return Rect(self.x, self.y, self.size.x, self.size.y)

    def collided_with(self, object, rect=None) -> Rect:
        if rect is None:
            rect = object.to_rect()
        return self.to_rect().clip(rect)

    def set_size_with_sprite(self):
        self.size = Axis(self.sprite.get_width(), self.sprite.get_height())
        self.glow = transform.smoothscale(self.glow, self.size.scale_to(1.2).to_list())

    def get_middle(self):
        return Axis(self.x + self.size.x / 2, self.y + self.size.y / 2)

    def center(self):
        self.x -= self.size.x / 2
        self.y -= self.size.y / 2

    def render(self, screen, glow=True):
        if glow:
            screen.blit(self.glow, (self.x-(self.size.x*0.12), self.y-(self.size.y*0.12)))

        screen.blit(self.sprite, self.to_rect())
