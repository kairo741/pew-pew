from .Player import Player
from .Axis import Axis
from .Ultimate import Ultimate
from lib.utils.Constants import Constants
from lib.utils.Utils import Utils
from random import randint


class PlayerFroggers(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", bullet_manager=None,
                 level=1):
        self.bullet_manager = bullet_manager
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate, duration=6,
                            color=[5, 109, 98])
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level=level)
        self.old_weapon_type = None
        self.old_shoot_delay = None

    def player_passive(self, render_frame_time):
        pass

    def enable_ultimate(self):
        for bullet in self.bullet_manager.bullets:
            bullet.tag = Constants.TAG_PLAYER
            bullet.sprite = Utils.scale_image(Constants.SPRITE_BULLET_FROGGERS_ULT, 0.4)
            # bullet.calculate_glow_color()
            bullet.glow_scale = 0
            if randint(1, 3) == 1:
                bullet.speed = Axis.zero()

        self.old_weapon_type = self.weapon.weapon_type
        self.old_shoot_delay = self.weapon.shoot_delay
        self.weapon.shoot_delay = 50
        self.weapon.weapon_type = 'explosion'

    def disable_ultimate(self):
        self.weapon.weapon_type = self.old_weapon_type
        self.weapon.shoot_delay = self.old_shoot_delay
