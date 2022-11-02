from random import uniform

import pygame

from lib.object.game.Axis import Axis
from lib.object.structure.Sound import Sound
from lib.utils.Constants import Constants


class Engine:
    def __init__(self, fullscreen=False, volume=...):
        super().__init__()
        self.resolution = None
        pygame.display.set_icon(Constants.SPRITE_PLAYER_SHIP_32x32)
        pygame.display.set_caption(Constants.WINDOW_CAPTION)
        pygame.display.init()
        pygame.joystick.init()
        pygame.font.init()

        self.base_flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL | pygame.SCALED
        self.flags = self.base_flags
        self.get_res = pygame.display.Info()

        self.is_fullscreen = fullscreen
        self.update_fullscreen_flags(self.is_fullscreen)
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

        self.sound = Sound(volume=volume)

    def fullscreen_mode(self):
        self.update_fullscreen_flags(not self.is_fullscreen)

        self.screen = pygame.display.set_mode(self.resolution.to_list(), self.flags)
        self.is_fullscreen = not self.is_fullscreen

    def update_fullscreen_flags(self, is_fullscreen):
        if is_fullscreen:
            self.resolution = Axis(x=int(self.get_res.current_w),
                                   y=int(self.get_res.current_h))
            self.flags = self.base_flags | pygame.FULLSCREEN
        else:
            self.resolution = Axis(x=int(self.get_res.current_w * 0.8),
                                   y=int(self.get_res.current_h * 0.8))
            self.flags = self.base_flags

    def check_quit_event_only(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def toggle_sound(self):
        if self.sound.is_sound_paused:
            self.sound.unmute()
        else:
            self.sound.mute()

    def shake_screen(self, value):
        value *= (self.resolution.x / 1000)
        self.screen_pos = Axis(uniform(-value, value), uniform(-value, value))
