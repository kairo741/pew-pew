from copy import deepcopy
from random import randrange, randint
from .GameObject import GameObject
from .Axis import Axis
from pygame import time, draw


class Background(GameObject):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), star_sprite=""):
        super().__init__(x, y, size, speed)
        self.star_sprite = star_sprite

    stars = []
    last_render_tick = 0
    star_render_delay_min = 500
    star_render_delay_max = 600
    star_spawn_position = Axis(-10, -30)

    def make_stars(self, screen_size):
        get_random_delay = randrange(
            self.star_render_delay_min, self.star_render_delay_max)
        last_pos = deepcopy(self.star_spawn_position)

        if time.get_ticks() - self.last_render_tick > get_random_delay:

            for i in range(0, randrange(5, 15)):
                self.stars.append(GameObject(x=randrange(0, screen_size[0]), y=randrange(-50, -10),
                                             speed=Axis(0, randrange(4, 15)), sprite=self.star_sprite))

            self.last_render_tick = time.get_ticks()

    def render_background(self, screen):
        screen_size = screen.get_size()
        self.make_stars(screen_size)

        draw.rect(screen, (14, 6, 21), (0, 0, screen_size[0], screen_size[1]), width=0)

        for star in self.stars:
            star.y += star.speed.y
            star.render(screen)
