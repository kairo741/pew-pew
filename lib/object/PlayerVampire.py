from pygame import Surface, transform

from lib.object.Ultimate import Ultimate
from .Player import Player
from .BulletVamp import BulletVamp
from .Axis import Axis
from random import uniform, choice
from lib.utils.Utils import Utils
from lib.utils.Constants import Constants


class PlayerVampire(Player):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", weapon="", health=100, layout="",
                 level=1,
                 sprite_ult=Surface((0, 0)), bullet_manager=None):
        self.bullet_manager = bullet_manager
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate,
                            color=[13, 1, 36])

        super().__init__(x, y, size, speed, sprite, weapon, health, layout, level=level, ultimate=ultimate)
        self.sprite_ult = sprite_ult

    def enable_ultimate(self):
        super().enable_ultimate()
        self.sprite = transform.smoothscale(self.sprite_ult, self.size.to_list())

        for index in range(100):
            sprite = Utils.scale_image(
                choice([Constants.SPRITE_BAT_1, Constants.SPRITE_BAT_2, Constants.SPRITE_BAT_3,
                        Constants.SPRITE_BAT_4]),
                0.1).convert_alpha()
            bat = BulletVamp(x=0, y=index * 10, speed=Axis(uniform(2, 10), 0),
                             sprite=sprite,
                             size=Axis(sprite.get_width(), sprite.get_height()),
                             damage=100,
                             tag=Constants.TAG_PLAYER,
                             source_reference=self)
            self.bullet_manager.bullets.append(bat)

    def disable_ultimate(self):
        self.sprite = transform.smoothscale(self.initial_sprite, self.size.to_list())
        super().disable_ultimate()
