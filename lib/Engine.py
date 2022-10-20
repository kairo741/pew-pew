
import pygame

from lib.object.game.Axis import Axis
from lib.utils.Constants import Constants


class Engine:
    def __init__(self):
        super().__init__()
        pygame.display.set_icon(Constants.SPRITE_PLAYER_SHIP_32x32)
        pygame.display.set_caption(Constants.WINDOW_CAPTION)
        pygame.display.init()
        pygame.joystick.init()
        pygame.font.init()
        pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT, pygame.JOYBUTTONDOWN, Constants.ULTIMATE_END])

        self.base_flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL | pygame.SCALED
        self.flags = self.base_flags

        self.is_fullscreen = False

        self.get_res = pygame.display.Info()
        self.resolution = Axis(
            x=int(self.get_res.current_w * 0.95),
            y=int(self.get_res.current_h * 0.95))
        self.real_screen = pygame.display.set_mode(
            size=self.resolution.to_list(),
            flags=self.flags,
            depth=24,
            vsync=1
        )

        self.screen = self.real_screen.copy()
        self.screen_pos = Axis(0, 0)

        self.clock = pygame.time.Clock()
        self.render_frame_time = 0

        self.joysticks = []

        
    def fullscreen_mode(self):
        if self.is_fullscreen:
            self.resolution = Axis(x=int(self.get_res.current_w * 0.95),
                                   y=int(self.get_res.current_h * 0.95))
            self.flags = self.base_flags
        else:
            self.resolution = Axis(x=int(self.get_res.current_w),
                                   y=int(self.get_res.current_h))
            self.flags = self.base_flags | pygame.FULLSCREEN

        self.screen = pygame.display.set_mode(self.resolution.to_list(), self.flags)
        self.is_fullscreen = not self.is_fullscreen
        

