from pygame import time
from lib.object.visual.Background import Background

from lib.object.game.Ultimate import Ultimate
from lib.utils.Constants import Constants


class UltimateManager:
    def __init__(self, background: Background):
        self.background = background

        self.disable_ultimate_function = lambda: None
        self.ultimate_enabled = False
        self.ult_tick = 0
        self.shake_duration = 0
        
    def get_shake_enabled(self):
        return self.ultimate_enabled and self.get_time_passed() < self.shake_duration

    def get_time_passed(self):
        return time.get_ticks() - self.ult_tick

    def do_ultimate(self, ultimate: Ultimate) -> bool:
        if self.ultimate_enabled is not True:
            self.ultimate_enabled = True
            self.ult_tick = time.get_ticks()
            self.shake_duration = ultimate.shake_duration
            self.background.change_bg_color(ultimate.color)

            ultimate.enable_function()
            
            self.disable_ultimate_function = ultimate.disable_function

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
