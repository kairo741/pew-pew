from .GameObject import GameObject
from lib.object.game.Axis import Axis
from lib.utils.Constants import Constants
from pygame import Surface, draw


class Ship(GameObject):
    def __init__(
            self,
            x=0,
            y=0,
            size=Axis.zero(),
            speed=Axis.zero(),
            sprite="",
            weapon="",
            health=100,
            tag=Constants.TAG_PLAYER,
            level=1,
            crit_rate=-1
    ):
        super().__init__(x, y, size, speed, sprite)

        self.weapon = weapon
        self.health = health
        self.max_health = health
        self.base_health = health
        self.last_bullet = 0
        self.initial_position = Axis(x, y)
        self.initial_sprite = sprite
        self.tag = tag
        self.level = level
        self.crit_rate = crit_rate
        self.set_level(self.level)

    def get_health_multiplier(self):
        return self.level ** 2 / 50

    def get_damage_multiplier(self):
        return self.level ** 2 / 50

    def set_level(self, level):
        if level > 100:
            level = 100
        self.level = level
        self.health = self.base_health + (self.base_health * self.get_health_multiplier())
        self.max_health = self.health
        if self.weapon is not None and self.weapon is not "":
            self.weapon.level = level

    def reset(self):
        self.x = self.initial_position.x
        self.y = self.initial_position.y
        self.set_level(1)
        self.revive()

    def disable(self):
        self.sprite = Surface((0, 0))
        self.size = Axis(0, 0)

    def revive(self):
        self.health = self.max_health
        self.last_bullet = 0
        self.sprite = self.initial_sprite.copy()
        self.set_size_with_sprite(set_glow=False)

    def set_size_with_sprite(self, set_glow=True):
        self.initial_sprite = self.sprite.copy()
        return super().set_size_with_sprite(set_glow)

    def is_alive(self):
        return self.health > 0

    def take_damage(self, value):
        self.health -= value

    def render_level(self, screen, align="bottom", space_bottom=1.6):
        if self.is_alive():
            this_font = Constants.FONT_LEVEL_OBJECT
            red = 255
            green = 255 * (1 - self.level / 100)
            blue = 255 / self.level

            text = this_font.render(str(self.level), True, (red, green, blue))
            text_size = text.get_size()
            if align == "bottom":
                screen.blit(text, (self.x + self.size.x / 2 - text_size[0] / 2, self.y + self.size.y * space_bottom))

            elif align == "top":
                screen.blit(text, (self.x + self.size.x / 2 - text_size[0] / 2, self.y - self.size.y * 0.6))

    def render_lifebar(self, screen, align="bottom", color=Constants.COLOR_GREEN):
        lifebar_size = Axis(self.size.x, self.size.y / 10)

        if align == "bottom":
            pos_y = self.size.y + self.y + lifebar_size.y * 2

        elif align == "top":
            pos_y = self.y - lifebar_size.y * 2

        health_size = lifebar_size.x * (self.health / self.max_health)
        draw.rect(screen, Constants.COLOR_RED,
                  (self.x, pos_y, lifebar_size.x, lifebar_size.y))
        draw.rect(screen, color, (self.x, pos_y, health_size, lifebar_size.y))
