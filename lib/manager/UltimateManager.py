from pygame import time
from lib.object.Background import Background

from lib.object.Ultimate import Ultimate
from lib.utils.Constants import Constants


class UltimateManager:
    def __init__(self, background: Background):
        self.background = background

        self.ultimate_enabled = False

        self.disable_ultimate_function = lambda: None

    def do_ultimate(self, ultimate: Ultimate) -> bool:
        if self.ultimate_enabled is not True:
            ultimate.enable_function()

            self.disable_ultimate_function = ultimate.disable_function
            self.ultimate_enabled = True
            self.background.change_bg_color(ultimate.color)

            time.set_timer(Constants.ULTIMATE_END, ultimate.duration * 1000, loops=1)

            return True

        return False

    def disable_ultimate(self):
        self.disable_ultimate_function()
        self.ultimate_enabled = False
        self.background.reset_bg_color()

    def reset(self):
        if self.ultimate_enabled:
            self.disable_ultimate()
