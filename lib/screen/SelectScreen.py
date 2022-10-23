from random import uniform
from threading import Thread
import pygame
from lib.Engine import Engine
from lib.object.game.Axis import Axis
from lib.object.visual.Background import Background
from .GameScreen import GameScreen


class SelectScreen:
    def __init__(self, engine: Engine, bg=Background()):
        self.engine = engine

        from lib.manager.PlayerManager import PlayerManager
        self.player_manager = PlayerManager(time_stop_ultimate=lambda: None, bullet_manager=None)
        self.player_manager.fetch_player_details(self.engine.resolution)
        self.current_player = 0
        self.selected_players = []

        self.bg = bg

        self.goto_menu = False
        self.animation_start = 0
        self.animation = False

        self.game_screen = None

    def tick_clock(self):
        self.render_frame_time = self.engine.clock.tick() / 10

    def start_animation(self):
        self.animation = True
        self.animation_start = pygame.time.get_ticks()

    def make_game_screen(self):
        self.game_screen = GameScreen(engine=self.engine, players_id=self.selected_players, bg=self.bg)

    def goto_game(self):
        self.bg.to_default()

        res = self.game_screen.start()
        if res:
            self.goto_menu = True
            
    def start(self):
        while True:
            self.tick_clock()
            
            self.bg.render_background(self.engine.screen, self.engine.resolution)
            self.bg.manage_stars(self.render_frame_time)

            if self.animation:
                self.engine.check_quit_event_only()
                self.manage_animation()
            else:
                self.game_events()
                self.render_current_player()

            for index, player_index in enumerate(self.selected_players):
                detail = self.player_manager.players[player_index]
                space = (index+1)*(self.engine.resolution.x/15)
                y = self.engine.resolution.y*0.6

                if self.animation:
                    time_diff = (pygame.time.get_ticks() - self.animation_start)
                    calc = ((time_diff/50)**2)/400
                    y -= calc * y
                
                detail.render_icon(self.engine.screen, self.engine.resolution.x/3 + space, y)

            if self.goto_menu:
                break

            self.engine.real_screen.blit(self.engine.screen, self.engine.screen_pos.to_list())
            pygame.display.update()


    def manage_animation(self):
        self.bg.star_render_delay = 25
        self.bg.speed = 16

        if pygame.time.get_ticks() - self.animation_start > 2000:
            self.goto_game()

    def render_current_player(self):
        player = self.player_manager.get_player(self.current_player)
        player.render(self.engine.screen)
        player.render_stats(self.engine.screen)

        # player.render_description(self.engine.screen, 1000, 0)

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
                    else:
                        self.goto_menu = True

                if event.key == pygame.K_RETURN:
                    if len(self.selected_players) > 0:
                        game_thread = Thread(target=self.make_game_screen)
                        game_thread.start()
                        self.start_animation()

                if event.key == pygame.K_F8:
                    self.engine.toggle_sound()

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
