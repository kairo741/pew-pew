from lib.utils.Constants import Constants
from lib.object.Number import Number
from pygame import time


class NumberManager:
    def __init__(self):
        super().__init__()
        self.numbers = []

    def add_damage_number(self, x, y, value, is_crit=False):
        dn = Number(x, y, round(value), time.get_ticks(), duration=800, 
            size=26 if not is_crit else 30, 
            color=Constants.COLOR_GREY if not is_crit else Constants.COLOR_YELLOW
        )
        self.numbers.append(dn)

    def add_take_damage_number(self, x, y, value):
        dn = Number(x, y, round(value), time.get_ticks(), color=Constants.COLOR_RED, duration=1000, size=36)
        self.numbers.append(dn)

    def add_heal_number(self, x, y, text):
        heal_number = Number(x, y, text, time.get_ticks(), color=Constants.COLOR_GREEN_HEAL, duration=1000, size=26)
        self.numbers.append(heal_number)

    def add_buff_info(self, x, y, text):
        info = Number(x, y, text, time.get_ticks(), color=Constants.COLOR_LIGHT_BLUE, duration=1000, size=26)
        self.numbers.append(info)

    def render(self, screen, render_frame_time):
        for number in self.numbers:
            time_left = (number.start_time + number.duration) - time.get_ticks()
            if time_left <= 0:
                self.numbers.remove(number)
            else:
                number.render(screen)
                number.opacity -= (255 / time_left) * (render_frame_time * 10)
                number.y -= 1 * render_frame_time
                number.x += 1 * render_frame_time
