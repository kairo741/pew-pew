from pygame import draw, time, mixer, font

from lib.object.Ultimate import Ultimate
from lib.utils.Constants import Constants
from .Axis import Axis
from .Ship import Ship


class Player(Ship):
    def __init__(self, x=0, y=0, size=Axis.zero(), speed=Axis.zero(), sprite="", weapon="", health=100, layout="",
                 ultimate=Ultimate(), level=1):
        super().__init__(x, y, size, speed, sprite, weapon, health, level=level)
        self.ultimate = ultimate
        self.layout = layout
        self.ult_cooldown_sec = 30
        self.next_ult = time.get_ticks() + 1000
        self.last_ult = 0
        self.is_invincible = False

        self.damage_dealt = 0

        
    def check_level_up(self):
        damage_required = self.damage_dealt / (500*self.level)
        if damage_required > self.level:
            if self.level < 100:
                self.set_level(self.level+1)


    def player_passive(self, render_frame_time):
        pass

    def take_damage(self, value):
        if self.is_invincible is not True:
            super().take_damage(value)
        if not self.is_alive():
            self.disable()

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

    def shoot(self, bullet_manager, damage_multiplier=1):
        if self.is_alive():
            if time.get_ticks() - self.last_bullet > self.weapon.shoot_delay:
                for generated_bullet in self.weapon.make_bullets(self.get_middle(), source_size=self.size):
                    generated_bullet.damage *= damage_multiplier
                    bullet_manager.shoot(generated_bullet)

                channel = mixer.Channel(Constants.SFX_MIXER_CHANNEL)
                # Constants.SFX_LASER.stop()
                channel.play(Constants.SFX_LASER)
                self.last_bullet = time.get_ticks()

    def ult(self, action):
        if self.is_alive():
            if self.next_ult < time.get_ticks():
                ult_enabled = action()

                if ult_enabled:
                    self.last_ult = time.get_ticks()
                    self.next_ult = self.last_ult + self.ult_cooldown_sec * 1000

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
        draw.rect(screen, (255, 40, 40), self.get_hitbox_rect(), border_radius=100)

    def render_ult_bar(self, screen):
        bar_size = Axis(self.size.x, self.size.y / 10)
        percentage = (time.get_ticks() - self.last_ult) / (self.next_ult - self.last_ult)
        cooldown_size = bar_size.x * percentage

        if cooldown_size > bar_size.x:
            cooldown_size = bar_size.x

        draw.rect(screen, Constants.COLOR_BLUE,
                  (self.x, self.y + self.size.y + bar_size.y * 4, cooldown_size, bar_size.y))

    def get_hitbox_rect(self):
        hitbox_size = Axis(self.size.x * 0.15, self.size.x * 0.15)
        middle = self.get_middle()
        middle.x -= hitbox_size.x / 2
        middle.y -= hitbox_size.x / 2
        return [middle.x, middle.y, hitbox_size.x, hitbox_size.y]

    def render(self, screen, render_frame_time):
        self.check_level_up()
        super().render(screen)
        self.render_level(screen)
        self.render_lifebar(screen, color=Constants.COLOR_GREEN if not self.is_invincible else Constants.COLOR_YELLOW)
        self.render_ult_bar(screen)
        self.render_hitbox(screen)
