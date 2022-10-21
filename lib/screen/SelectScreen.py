from random import uniform
import pygame
from lib.Engine import Engine
from lib.object.game.Axis import Axis
from lib.object.structure.Sound import Sound
from lib.object.visual.Background import Background
from .GameScreen import GameScreen


class SelectScreen:
    def __init__(self, engine=Engine()):
        self.engine = engine

        from lib.manager.PlayerManager import PlayerManager
        self.player_manager = PlayerManager(time_stop_ultimate=lambda: None, bullet_manager=None)
        self.player_manager.fetch_player_details()
        self.current_player = 0
        self.selected_players = []

        self.bg = Background()
        
        self.sound = Sound()
        self.sound.play_bg_music()
        self.sound.mute()

        self.goto_menu = False

    def tick_clock(self):
        self.render_frame_time = self.engine.clock.tick() / 10

    def goto_game(self):
        res = GameScreen(engine=self.engine, players_id=self.selected_players).start()
        if res:
            self.goto_menu = True


    def start(self):
        while True:
            if self.goto_menu:
                break
            
            self.tick_clock()
            self.game_events()

            self.bg.render_background(self.engine.screen, self.engine.resolution)
            self.bg.manage_stars(self.render_frame_time)

            self.player_manager.render_player(self.current_player, self.engine.screen)

            for index, player_index in enumerate(self.selected_players):
                detail = self.player_manager.players[player_index]
                space = (index+1)*(self.engine.resolution.x/15)
                detail.render_icon(self.engine.screen, self.engine.resolution.x/3 + space, self.engine.resolution.y*0.6)

            # pygame.draw.rect(self.engine.screen, (255, 255, 255), 
            #     (
            #         self.engine.resolution.x/3, 
            #         self.engine.resolution.y*0.6,
            #         4*(self.engine.resolution.x/15),
            #         200,
            #     ), 
            #     width=1, 
            #     border_radius=25,
            # )


            self.engine.real_screen.blit(self.engine.screen, self.engine.screen_pos.to_list())
            pygame.display.update()


    def toggle_sound(self):
        if self.sound.is_sound_paused:
            self.sound.unmute()
        else:
            self.sound.mute()

    def game_events(self):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if event.mod & pygame.KMOD_ALT:
                        self.engine.fullscreen_mode()

                if event.key == pygame.K_d:
                    self.change_player("d")

                if event.key == pygame.K_a:
                    self.change_player("a")

                if event.key == pygame.K_SPACE:
                    if len(self.selected_players) < 4:
                        self.selected_players.append(self.current_player)
                        self.current_player = 0

                if event.key == pygame.K_ESCAPE:
                    if len(self.selected_players) > 0:
                        self.selected_players.pop(len(self.selected_players)-1)
                        self.current_player = 0

                if event.key == pygame.K_RETURN:
                    if len(self.selected_players) > 0:
                        self.goto_game()

                if event.key == pygame.K_F8:
                    self.toggle_sound()

            if event.type == pygame.QUIT:
                pygame.quit()

    def change_player(self, direction):
        if direction == "d":
            self.current_player += 1
            if self.current_player > len(self.player_manager.players)-1:
                self.current_player = 0

        elif direction == "a":
            self.current_player -= 1
            if self.current_player < 0:
                self.current_player = len(self.player_manager.players)-1

    def shake_screen(self, value):
        value *= (self.engine.resolution.x / 1000)
        self.engine.screen_pos = Axis(uniform(-value, value), uniform(-value, value))
        

    def toggle_fullscreen(self):
        self.engine.fullscreen_mode()
        self.pause.copy_current_frame()
