from lib.object.game.Axis import Axis
from lib.object.bullets.Bullet import Bullet
from lib.utils.Constants import Constants
from random import uniform


class BulletBounce(Bullet):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", damage=10, tag=Constants.TAG_PLAYER,
                 source_reference=None, crit_rate=0):
        super().__init__(x, y, size, speed, sprite, damage, tag, source_reference, crit_rate)
        self.wall_bounce = 1
        

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


    def shoot_callback(self):
        super().shoot_callback()
        self.wall_bounce = self.source_reference.bounce_times


    def check_bullet(self, bullets, screen_size):
        if self.wall_bounce > 0:
            # self.speed = Axis(x=self.speed.x, y=-self.speed.y) #kkkkkk
            if self.y < -self.size.y:
                self.speed = Axis(x=self.speed.x + uniform(-15, 15), y=-self.speed.y)
                self.wall_bounce -= 1

            elif self.x < -self.size.x:
                self.speed = Axis(x=-self.speed.x + uniform(-15, 15), y=-self.speed.y)
                self.wall_bounce -= 1

            elif self.x > screen_size.x:
                self.speed = Axis(x=-self.speed.x, y=-self.speed.y)
                self.wall_bounce -= 1

            elif self.y > screen_size.y:
                self.speed = Axis(x=self.speed.x, y=-self.speed.y)
                self.wall_bounce -= 1
        else:
            if self.y < -self.size.y:
                bullets.remove(self)

            elif self.x < -self.size.x:
                bullets.remove(self)

            elif self.x > screen_size.x:
                bullets.remove(self)

            elif self.y > screen_size.y:
                bullets.remove(self)
