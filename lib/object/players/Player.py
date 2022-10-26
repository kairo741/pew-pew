from random import uniform
from pygame import Color, draw, time, mixer, Surface, time, Rect, SRCALPHA, mixer

from lib.object.game.Ultimate import Ultimate
from lib.utils.Constants import Constants
from lib.object.game.Axis import Axis
from lib.object.structure.Ship import Ship


class Player(Ship):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", weapon="", health=100, layout="",
                 ultimate=Ultimate(), level=1):
        super().__init__(x, y, size, speed, sprite, weapon, health, level=level)
        self.layout = layout

        self.ultimate = ultimate
        self.ult_cooldown_sec = 30
        self.next_ult = time.get_ticks() + 1000
        self.last_ult = 0

        self.is_invincible = False
        self.is_ulted = False
        self.ult_bar_hue = 0
        self.ult_tick = 0

        self.xp = 0
        self.crit_rate = 0.1

        self.old_glow_scale = 0

        self.recent_inputs = []
        self.last_input_tick = 0

        self.bonus_xp_multiplier = 0

    def enable_ultimate(self):
        self.ult_tick = time.get_ticks()
        self.is_ulted = True
        self.old_glow_scale = self.glow_scale
        self.glow_scale = 10
        self.glow_color = self.calculate_glow_color()
        self.set_glow()
        Constants.SFX_ULT_ENABLE.play()

    def disable_ultimate(self):
        self.is_ulted = False
        self.glow_scale = self.old_glow_scale
        self.glow_color = self.calculate_glow_color()
        self.set_glow()

    def check_level_up(self):
        damage_required = self.xp / (500 * self.level)
        if damage_required > self.level:
            if self.is_alive():
                self.set_level(self.level + 1)

    def add_xp(self, xp):
        self.xp += xp * self.bonus_xp_multiplier/4

    def player_passive(self, render_frame_time):
        pass

    def take_damage(self, value):
        if self.is_invincible is not True:
            super().take_damage(value)
        if not self.is_alive():
            self.disable()

    def record_input(self, input_code):
        size = len(self.recent_inputs)

        if size > 30:
            self.recent_inputs.pop(0)

        if time.get_ticks() - self.last_input_tick > 150:
            self.recent_inputs.append(input_code)
            self.last_input_tick = time.get_ticks()
            content = "".join(self.recent_inputs)

            if ("uuddlrlrba" in content):
                self.recent_inputs = []
                Constants.SFX_CODE.play()
                self.is_invincible = True
        

    def move(self, direction, render_frame_time, limit, multiplier=1):
        if self.is_alive():
            if direction == "r":
                if self.x + self.size.x < limit.x:
                    self.x += self.speed.x * multiplier * render_frame_time

            if direction == "l":
                if self.x > 2:
                    self.x -= self.speed.x * multiplier * render_frame_time

            if direction == "u":
                if self.y > 2:
                    self.y -= self.speed.y * multiplier * render_frame_time

            if direction == "d":
                if self.y + self.size.y < limit.y:
                    self.y += self.speed.y * multiplier * render_frame_time

        self.record_input(direction)

    def shoot(self, bullet_manager, damage_multiplier=1, shoot_delay_multiplier=1):
        if self.is_alive():
            if time.get_ticks() - self.last_bullet > self.weapon.shoot_delay*shoot_delay_multiplier:
                for generated_bullet in self.weapon.make_bullets(self.get_middle(), source_size=self.size):
                    generated_bullet.damage *= damage_multiplier
                    bullet_manager.shoot(generated_bullet)

                channel = mixer.Channel(Constants.MIXER_CHANNEL_SFX)
                channel.play(Constants.SFX_LASER)
                self.last_bullet = time.get_ticks()

        self.record_input("a")

    def ult(self, action):
        if self.is_alive():
            if self.next_ult < time.get_ticks():
                ult_enabled = action()

                if ult_enabled:
                    self.last_ult = time.get_ticks()
                    self.next_ult = self.last_ult + self.ult_cooldown_sec * 1000

            self.record_input("b")

    def control_ship(self, keys, render_frame_time, limit):
        if self.is_alive():
            if keys[self.layout.right]:
                self.move("r", render_frame_time, limit)

            if keys[self.layout.left]:
                self.move("l", render_frame_time, limit)

            if keys[self.layout.up]:
                self.move("u", render_frame_time, limit)

            if keys[self.layout.down]:
                self.move("d", render_frame_time, limit)

    def control_shoot(self, keys, bullet_manager):
        if keys[self.layout.shoot]:
            self.shoot(bullet_manager)

    def control_ultimate(self, keys, action):
        if keys[self.layout.ultimate]:
            self.ult(action)

    def control_ship_joystick(self, joystick, render_frame_time, limit):
        axis = Axis(joystick.get_axis(0), joystick.get_axis(1))

        if axis.x > self.layout.right:
            self.move("r", render_frame_time, limit, multiplier=axis.x)

        if axis.x < self.layout.left:
            self.move("l", render_frame_time, limit, multiplier=-axis.x)

        if axis.y < self.layout.up:
            self.move("u", render_frame_time, limit, multiplier=-axis.y)

        if axis.y > self.layout.down:
            self.move("d", render_frame_time, limit, multiplier=axis.y)

    def control_shoot_joystick(self, joystick, bullet_manager):
        if joystick.get_button(self.layout.shoot):
            self.shoot(bullet_manager)

    def control_ultimate_joystick(self, joystick, action):
        if joystick.get_button(self.layout.ultimate):
            self.ult(action)

    def render_hitbox(self, screen):
        shape_surf = Surface(Rect(self.get_hitbox_rect()).size, SRCALPHA)
        draw.rect(shape_surf, (255, 40, 40), shape_surf.get_rect())
        screen.blit(shape_surf, self.get_hitbox_rect())

    def render_ult_bar(self, screen):
        bar_size = Axis(self.size.x, self.size.y / 10)
        if not self.is_ulted:

            percentage = (time.get_ticks() - self.last_ult) / (self.next_ult - self.last_ult)
            cooldown_size = bar_size.x * percentage

            if cooldown_size > bar_size.x:
                cooldown_size = bar_size.x

            draw.rect(screen, Constants.COLOR_BLUE,
                    (self.x, self.y + self.size.y + bar_size.y * 4, cooldown_size, bar_size.y))

        else:
            self.ult_bar_hue = self.ult_bar_hue + 2 if self.ult_bar_hue < 359 else 0
            bar_color = Color(0)
            bar_color.hsla = ((self.ult_bar_hue, 100, 70, 70))
            bar_size.x *= 1-(time.get_ticks()-self.ult_tick) / (self.ultimate.duration*1000)

            draw.rect(screen, bar_color,
                    (self.x+uniform(-5, 5), self.y+uniform(-5, 5) + self.size.y + bar_size.y * 4, bar_size.x, bar_size.y))

    def get_hitbox_rect(self):
        hitbox_size = Axis(self.size.x * 0.1, self.size.x * 0.1)
        middle = self.get_middle()
        middle.x -= (hitbox_size.x / 2)
        middle.y -= hitbox_size.x / 2
        return [middle.x, middle.y, hitbox_size.x + 1, hitbox_size.y]

    def render(self, screen, render_frame_time, hide_hud=False):
        self.check_level_up()
        super().render(screen)
        if not hide_hud:
            self.render_level(screen)
            self.render_lifebar(screen, color=Constants.COLOR_GREEN if not self.is_invincible else Constants.COLOR_YELLOW)
            self.render_ult_bar(screen)
            self.render_hitbox(screen)
