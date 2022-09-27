import pygame
from lib.Engine import Engine
from lib.object.structure.Sound import Sound
from lib.object.visual.Background import Background
from lib.utils.Constants import Constants


class MenuScreen:
    def __init__(self):
        self.engine = Engine()

        self.bg = Background()

        self.sound = Sound()
        self.sound.play_bg_music()
        #self.sound.mute()

    def start(self):
        while True:
            self.tick_clock()
            # self.game_events()

            self.render_frame_time = self.engine.clock.tick() / 10

            self.bg.render_background(
                self.engine.screen, self.engine.resolution)

            self.bg.manage_stars(self.render_frame_time)

            pygame.display.update()

    def tick_clock(self):
        self.render_frame_time = self.engine.clock.tick() / 10

    def game_events(self):
        self.player_input()
        self.update_controller_state()

        for event in pygame.event.get():
            if self.state == Constants.PAUSE:
                self.pause.check_pause_events(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()

                if event.key == pygame.K_ESCAPE:
                    if self.state == Constants.PAUSE:
                        self.pause.stop_pause()
                        self.state = Constants.RUNNING
                    else:
                        self.pause.start_pause()
                        self.state = Constants.PAUSE

                if event.key == pygame.K_RETURN:
                    if event.mod & pygame.KMOD_ALT:
                        self.engine.fullscreen_mode()

                    elif not self.round_started:
                        self.round_started = True

                if event.key == pygame.K_F8:
                    self.toggle_sound()

                self.reset_keys(event.key)

            if event.type == pygame.JOYBUTTONDOWN and event.button == 6:
                if self.state == Constants.PAUSE:
                    self.pause.stop_pause()
                    self.state = Constants.RUNNING
                else:
                    self.pause.start_pause()
                    self.state = Constants.PAUSE

            if event.type == Constants.ULTIMATE_END:
                self.ultimate_manager.disable_ultimate()

            if event.type == pygame.QUIT:
                pygame.quit()
