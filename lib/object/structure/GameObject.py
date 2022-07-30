from copy import deepcopy
from pygame import BLEND_MULT, Rect, Surface, transform, draw

from lib.object.game.Ultimate import Ultimate
from lib.object.game.Axis import Axis
from lib.utils.Constants import Constants


class GameObject:
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", glow_scale=2):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.sprite = sprite
        self.glow = Constants.SPRITE_GLOW.convert_alpha()
        self.glow_scale = glow_scale
        self.glow_color = None

    def copy(self):
        copy_obj = type(self)()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                if type(attr) is Ultimate:
                    copy_obj.__dict__[name] = attr.copy(parent=copy_obj)
                else:
                    copy_obj.__dict__[name] = attr.copy()
            else:
                if type(attr) is Surface:
                    copy_obj.__dict__[name] = Surface.copy(attr)
                else:
                    copy_obj.__dict__[name] = deepcopy(attr)
        return copy_obj

    def to_rect(self):
        return Rect(self.x, self.y, self.size.x, self.size.y)

    def collided_with(self, object, rect=None) -> Rect:
        if rect is None:
            rect = object.to_rect()
        return self.to_rect().clip(rect)

    def set_size_with_sprite(self, set_glow=True):
        self.size = Axis(self.sprite.get_width(), self.sprite.get_height())
        if set_glow:
            self.set_glow()

    def calculate_glow_color(self):
        average_color = [0, 0, 0, 255]
        # loop em todos os pixels da sprite
        for x in range(self.size.x):
            for y in range(self.size.y):
                this_color = self.sprite.get_at((x, y))

                # se esse pixel nao for transparente
                if this_color[3] != 0:
                    brightness = (this_color[0] + this_color[1] + this_color[2]) / (255 * 3)

                    if brightness < 0.8:
                        this_color = this_color.correct_gamma(0.8)
                        if brightness < 0.11:
                            this_color = this_color.correct_gamma(0.1)

                        # adicionar essa cor
                        for i in range(0, 3):
                            average_color[i] += this_color[i]

        try:
            for i in range(0, 3):
                average_color[i] /= (self.size.x * self.size.y)

        except:
            print("color division error")
            average_color = (255, 255, 255)


        self.glow_color = average_color

    def set_glow(self):
        if self.glow_scale > 0:
            if self.glow_color is None:
                self.calculate_glow_color()

            glow_size = self.size.scale_to(self.glow_scale).to_list()
            self.glow = Constants.SPRITE_GLOW.copy().convert_alpha()
            self.glow = transform.smoothscale(self.glow, glow_size)
            color_surf = Surface(glow_size)
            color_surf.fill(self.glow_color)
            
            self.glow.blit(color_surf, (0, 0), special_flags=BLEND_MULT)

    def get_hitbox_rect(self):
        return [self.x, self.y, self.size.x, self.size.y]

    def get_middle(self):
        return Axis(self.x + self.size.x / 2, self.y + self.size.y / 2)

    def center(self):
        self.x -= self.size.x / 2
        self.y -= self.size.y / 2

    def render(self, screen, show_hitbox=False):
        if self.glow_scale > 0:
            glow_difference = Axis((self.size.x * self.glow_scale) - self.size.x,
                                   (self.size.y * self.glow_scale) - self.size.y)
            screen.blit(self.glow, (self.x - glow_difference.x / 2, self.y - glow_difference.y / 2))

        if show_hitbox:
            draw.rect(screen, (255, 255, 255), self.get_hitbox_rect(), 1)

        screen.blit(self.sprite, self.to_rect())
