from pygame import time
from lib.object.Ultimate import Ultimate
from lib.utils.Constants import Constants


class UltimateManager():
    def __init__(self, background):
        self.background = background
        
        self.ultimate_enabled = False

        self.disable_ultimate_function = lambda: None

    def do_ultimate(self, ultimate: Ultimate) -> bool:
        if self.ultimate_enabled is not True:
            ultimate.enable_function()

            self.disable_ultimate_function = ultimate.disable_function
            self.ultimate_enabled = True
            self.background.color = [code + 50 for code in self.background.color]

            time.set_timer(Constants.ULTIMATE_END, ultimate.duration*1000)
            

            return True
        
        return False


    def disable_ultimate(self):
        self.disable_ultimate_function()
        self.ultimate_enabled = False
        self.background.color = Constants.BACKGROUND_COLOR


    def reset(self):
        self.disable_ultimate()