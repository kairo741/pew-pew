from random import choice

import pygame

from lib.utils.Constants import Constants


class Sound:
    def __init__(self, volume=Constants.VOLUME_GLOBAL):
        self.volume_global = volume/2
        self.volume_sfx = self.volume_global * 0.9
        self.volume_effects = self.volume_global * 1
        self.volume_bgm = self.volume_global * 0.5

        # Define channels
        self.sound_channel_sfx = pygame.mixer.Channel(Constants.MIXER_CHANNEL_SFX)
        self.sound_channel_bgm = pygame.mixer.Channel(Constants.MIXER_CHANNEL_BGM)
        self.sound_channel_enemy = pygame.mixer.Channel(Constants.MIXER_CHANNEL_ENEMY)
        self.sound_channel_effects = pygame.mixer.Channel(Constants.MIXER_CHANNEL_EFFECTS)
        self.sound_channel_ult = pygame.mixer.Channel(Constants.MIXER_CHANNEL_ULT)
        # Set Volume
        self.set_volume()

        self.font = pygame.font.SysFont("Segoe UI Symbol", 34)
        self.is_sound_paused = False

    def mute(self):
        self.sound_channel_sfx.set_volume(0)
        self.sound_channel_sfx.pause()
        self.sound_channel_bgm.set_volume(0)
        self.sound_channel_bgm.pause()
        self.sound_channel_enemy.set_volume(0)
        self.sound_channel_enemy.pause()
        self.sound_channel_effects.set_volume(0)
        self.sound_channel_effects.pause()
        self.sound_channel_ult.set_volume(0)
        self.sound_channel_ult.pause()
        self.is_sound_paused = True

    def unmute(self):
        self.set_volume()
        self.sound_channel_sfx.unpause()
        self.sound_channel_bgm.unpause()
        self.sound_channel_enemy.unpause()
        self.sound_channel_effects.unpause()
        self.sound_channel_ult.unpause()
        self.is_sound_paused = False

    def set_volume(self):
        self.sound_channel_sfx.set_volume(self.volume_sfx)
        self.sound_channel_effects.set_volume(self.volume_effects)
        self.sound_channel_bgm.set_volume(self.volume_bgm)
        self.sound_channel_enemy.set_volume(self.volume_sfx)
        self.sound_channel_ult.set_volume(self.volume_effects)

    def play_random_bg_music(self):
        self.sound_channel_bgm.play(choice(Constants.BGM_LIST), -1, fade_ms=1500)

    def play_menu_music(self):
        self.sound_channel_bgm.play(Constants.BGM_INFINITY, -1, fade_ms=1500)

    def render_muted_icon(self, screen, resolution):
        text = self.font.render('🔇', True, (255, 255, 255))
        screen.blit(text, [resolution.x - 40, 10])
