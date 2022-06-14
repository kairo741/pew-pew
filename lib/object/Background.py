from copy import deepcopy
from random import randrange
from .GameObject import GameObject
from .Axis import Axis
from pygame import time, draw


class Background(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), star_sprite=""):
        super().__init__(x, y, size, speed)

    stars = []
    last_render_tick = 0
    star_render_delay_min = 1000
    star_render_delay_max = 5000
    star_spawn_position = Axis(-10, -30)


    def make_stars(self, screen_size):
        get_random_delay = randrange(
            self.star_render_delay_min, self.star_render_delay_max)
        last_pos = deepcopy(self.star_spawn_position)

        if time.get_ticks() - self.last_render_tick > get_random_delay:
            while(last_pos.x < screen_size[0]):
                last_pos.x = randrange(last_pos.x+10, last_pos.x+90)
                last_pos.y += randrange(-50, -10)

                self.stars.append(GameObject(x=last_pos.x, y=last_pos.y, speed=Axis(
                    0, randrange(4, 30)), sprite=self.star_sprite))
                self.last_render_tick = time.get_ticks()

    def render_background(self, screen):
        screen_size = screen.get_size()
        self.make_stars(screen_size)
        
        draw.rect(screen, (14, 6, 21), (0, 0, screen_size[0], screen_size[1]), width=0)

        for star in self.stars:
            star.y += star.speed.y
            star.render(screen)
