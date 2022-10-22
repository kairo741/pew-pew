from random import randrange
from lib.utils.Constants import Constants
from lib.utils.Utils import Utils
from lib.object.structure.GameObject import GameObject
from lib.object.game.Axis import Axis
from pygame import time, draw


class Background(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero()):
        super().__init__(x, y, size)
        self.color = Constants.BACKGROUND_COLOR
        self.star_sprite = Utils.scale_image(Constants.SPRITE_STAR.convert_alpha(), 0.1)
        self.star_sprite.set_alpha(90)

        self.stars = []
        self.last_star_tick = 0
        self.star_render_delay = 500
        self.star_spawn_position = Axis(-10, -30)
        self.speed = 8

    def to_default(self):
        self.star_render_delay = 500
        self.speed = 8

    def create_star(self):
        return GameObject(x=randrange(0, self.size.x), y=randrange(-50, -10), speed=Axis(0, randrange(self.speed-4, self.speed+5)), sprite=self.star_sprite, glow_scale=0)

    def make_stars(self):
        get_random_delay = randrange(int(self.star_render_delay/10)+self.star_render_delay*2)

        if time.get_ticks() - self.last_star_tick > get_random_delay:

            for i in range(0, randrange(5, 15)):
                self.stars.append(self.create_star())

            self.last_star_tick = time.get_ticks()

    def manage_stars(self, render_frame_time):
        self.make_stars()
        for star in self.stars:
            star.y += star.speed.y * render_frame_time
            if (star.y > self.size.y):
                try:
                    self.stars.remove(star)
                except:
                    print("error removing star")


    def change_bg_color(self, color):
        self.color = color

    def reset_bg_color(self):
        self.color = Constants.BACKGROUND_COLOR

    
    def render_background(self, screen, resolution):
        self.size = resolution

        draw.rect(screen, self.color, self.to_rect())

        for star in self.stars:
            star.render(screen)
            
