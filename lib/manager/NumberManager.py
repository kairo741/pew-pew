from lib.utils.Constants import Constants
from lib.object.Number import Number
from pygame import time


class NumberManager:
    def __init__(self):
        super().__init__()
        self.numbers = []

    def add_damage_number(self, x, y, value):
        dn = Number(x, y, round(value), time.get_ticks(), color=Constants.COLOR_GREY, duration=500, size=26)
        self.numbers.append(dn)

    def add_take_damage_number(self, x, y, value):
        dn = Number(x, y, round(value), time.get_ticks(), color=Constants.COLOR_RED, duration=1000, size=36)
        self.numbers.append(dn)

    def add_heal_number(self, x, y, text):
        heal_number = Number(x, y, text, time.get_ticks(), color=Constants.COLOR_GREEN_HEAL, duration=1000, size=26)
        self.numbers.append(heal_number)

    def render(self, screen, render_frame_time):
        for number in self.numbers:
            time_left = (number.start_time + number.duration) - time.get_ticks()
            if time_left <= 0:
                self.numbers.remove(number)
            else:
                number.render(screen)
                number.opacity -= (255 / time_left) * (render_frame_time * 10)
