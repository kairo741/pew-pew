from pygame import Surface, transform, time, mixer

from lib.object.game.Ultimate import Ultimate
from lib.object.players.Player import Player
from lib.object.bullets.BulletVamp import BulletVamp
from lib.object.game.Axis import Axis
from random import uniform, choice
from lib.utils.Utils import Utils
from lib.utils.Constants import Constants


class PlayerVampire(Player):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", weapon="", health=100, layout="",
                 level=1,
                 sprite_ult=Surface((0, 0)), bullet_manager=None):
        self.bullet_manager = bullet_manager
        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate,
                            color=[13, 1, 36], duration=6, shake_duration=None)

        super().__init__(x, y, size, speed, sprite, weapon, health, layout, level=level, ultimate=ultimate)
        self.sprite_ult = sprite_ult

        self.last_bat = 0

    def player_passive(self, render_frame_time):
        if self.is_ulted:
            if time.get_ticks() - self.last_bat > 15:
                sprite = Utils.scale_image(
                    choice([Constants.SPRITE_BAT_1, Constants.SPRITE_BAT_2, Constants.SPRITE_BAT_3,
                            Constants.SPRITE_BAT_4]),
                    0.1).convert_alpha()

                bat = BulletVamp(x=self.x, y=self.y, speed=Axis(uniform(-5, 5), uniform(-5, -1)),
                                 sprite=sprite,
                                 size=Axis(sprite.get_width(), sprite.get_height()),
                                 damage=(self.weapon.bullet.damage + self.weapon.get_bonus_level_damage()) * 2,
                                 tag=Constants.TAG_PLAYER,
                                 source_reference=self,
                                 )
                self.bullet_manager.bullets.append(bat)
                self.last_bat = time.get_ticks()

        return super().player_passive(render_frame_time)

    def enable_ultimate(self):
        super().enable_ultimate()
        channel = mixer.Channel(Constants.MIXER_CHANNEL_EFFECTS)
        channel.play(Constants.SFX_VAMPIRE_ULT)
        self.sprite = transform.smoothscale(self.sprite_ult, self.size.to_list())

    def disable_ultimate(self):
        self.sprite = transform.smoothscale(self.initial_sprite, self.size.to_list())
        super().disable_ultimate()
