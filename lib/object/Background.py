from random import randrange

from utils.Constants import Constants
from utils.Utils import Utils
from .GameObject import GameObject
from .Axis import Axis
from pygame import time, draw


class Background(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero()):
        super().__init__(x, y, size)
        self.star_sprite = Utils.scale_image(Constants.SPRITE_STAR, 0.1)
        self.star_sprite.set_alpha(90)

    stars = []
    last_star_tick = 0
    star_render_delay = 500
    star_spawn_position = Axis(-10, -30)

    def create_star(self):
        return GameObject(x=randrange(0, self.size.x), y=randrange(-50, -10), speed=Axis(0, randrange(4, 15)), sprite=self.star_sprite)

    def make_stars(self):
        get_random_delay = randrange(
            self.star_render_delay-200+self.star_render_delay+200)

        if time.get_ticks() - self.last_star_tick > get_random_delay:

            for i in range(0, randrange(5, 15)):
                self.stars.append(self.create_star())

            self.last_star_tick = time.get_ticks()

    def manage_stars(self, render_frame_time):
        self.make_stars()
        for star in self.stars:
            star.y += star.speed.y * render_frame_time
            if (star.y > self.size.x):
                try:
                    self.stars.remove(star)
                except:
                    print("error removing star")
    
    def render_background(self, screen, resolution):
        self.size = resolution

        draw.rect(screen, (14, 6, 21), self.to_rect())

        for star in self.stars:
            star.render(screen)
            
