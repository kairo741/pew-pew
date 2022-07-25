from lib.object.Axis import Axis
from lib.object.Ultimate import Ultimate
from .Player import Player

from pygame import Surface, transform

class PlayerSpeed(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout=""):
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate, duration=8)

        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate)

        self.rotate = 0
        self.old_sprite = Surface((0, 0))
        self.old_speed = Axis(0, 0)



    def enable_ultimate(self):
        self.old_sprite = self.sprite
        self.old_speed = self.speed
        self.speed = self.speed.scale_to(1.5)
        self.rotate = 1
        self.is_invincible = True
        

    def disable_ultimate(self):
        self.sprite = self.old_sprite
        self.rotate = 0
        self.is_invincible = False

    def render(self, screen, render_frame_time):
        if self.rotate != 0:
            self.sprite = transform.rotate(self.old_sprite, self.rotate)
            self.sprite = transform.scale(self.sprite, self.size.to_list())

            self.rotate-=10
            print(self.rotate)
            if self.rotate < -359:
                self.rotate = 1

            

        return super().render(screen, render_frame_time)