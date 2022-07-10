from utils.Constants import Constants
from object.Number import Number
from pygame import time

class NumberManager:
    def __init__(self):
        super().__init__()
        self.numbers = []

    def add_damage_number(self, x, y, value):
        dn = Number(x, y, value, time.get_ticks(), color=Constants.COLOR_GREY, duration=300, size=26)
        self.numbers.append(dn)

    def add_take_damage_number(self, x, y, value):
        dn = Number(x, y, value, time.get_ticks(), color=Constants.COLOR_RED, duration=1000, size=36)
        self.numbers.append(dn)

    def render(self, screen):
        for number in self.numbers:
            time_left = (number.start_time + number.duration) - time.get_ticks()
            if time_left <= 0:
                self.numbers.remove(number)
            else:
                number.render(screen)
                number.opacity-=(255/time_left)

            
