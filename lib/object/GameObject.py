from pygame import BLEND_MULT, Rect, Surface, transform, draw
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
        self.glow_scale = 2.8

    def to_rect(self):
        return Rect(self.x, self.y, self.size.x, self.size.y)

    def collided_with(self, object, rect=None) -> Rect:
        if rect is None:
            rect = object.to_rect()
        return self.to_rect().clip(rect)

    def set_size_with_sprite(self):
        self.size = Axis(self.sprite.get_width(), self.sprite.get_height())
        self.set_glow()
        

    def set_glow(self):
        glow_size = self.size.scale_to(self.glow_scale).to_list()

        self.glow = transform.smoothscale(self.glow, glow_size)
        color_surf = Surface(glow_size)

        average_color = [0, 0, 0, 255]
        # loop em todos os pixels da sprite
        for x in range(self.size.x):
            for y in range(self.size.y):
                this_color = self.sprite.get_at((x, y))

                # se esse pixel nao for transparente
                if this_color[3] != 0:
                    # adicionar essa cor
                    for i in range(0, 3):
                        average_color[i] += this_color[i]

        for i in range(0, 3):
            average_color[i] /= (self.size.x*self.size.y)

        # desenhar cor mantendo transparencia
        color_surf.fill(average_color)
        self.glow.blit(color_surf, (0, 0), special_flags=BLEND_MULT)
        
    def get_hitbox_rect(self):
        return [self.x, self.y, self.size.x, self.size.y]

    def get_middle(self):
        return Axis(self.x + self.size.x / 2, self.y + self.size.y / 2)

    def center(self):
        self.x -= self.size.x / 2
        self.y -= self.size.y / 2

    def render(self, screen, glow=True, show_hitbox=False):
        if glow:
            glow_difference = Axis((self.size.x*self.glow_scale)-self.size.x, (self.size.y*self.glow_scale)-self.size.y)
            screen.blit(self.glow, (self.x-glow_difference.x/2, self.y-glow_difference.y/2))
        if show_hitbox:
            draw.rect(screen, (255, 255, 255), self.get_hitbox_rect(), 1)

        screen.blit(self.sprite, self.to_rect())
