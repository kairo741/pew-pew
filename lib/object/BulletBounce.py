from copy import deepcopy

from pygame import Surface

from lib.object.Axis import Axis
from lib.object.Bullet import Bullet
from lib.utils.Constants import Constants


class BulletBounce(Bullet):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", damage=10, tag=Constants.TAG_PLAYER,
                 source_reference=None):
        super().__init__(x, y, size, speed, sprite, damage, tag, source_reference)

    def hit_callback(self, object_hit, collision):
        super().hit_callback(object_hit, collision)
        hits = [edge for edge in ['left', 'right'] if getattr(collision, edge) == getattr(self.to_rect(), edge)]
        self.speed = Axis(x=self.speed.x, y=-self.speed.y)
        speed_x = abs(self.speed.x)
        speed_y = abs(self.speed.y)
        horizontal_speed = speed_y if speed_y > speed_x else speed_x

        for hit in hits:
            if hit == "left":
                self.speed.x = horizontal_speed
            elif hit == "right":
                self.speed.x = -horizontal_speed
