import pygame
from object.Axis import Axis
from object.Background import Background
from object.Fps import FPS
from object.Score import Score
from object.Player import Player
from utils.Constants import Constants
from utils.Presets import Presets
from utils.Utils import Utils

from .BulletManager import BulletManager
from .EnemyManager import EnemyManager
from .PlayerManager import PlayerManager
from .ItemManager import ItemManager


class GameManager:
    def __init__(self):
        super().__init__()
        pygame.display.set_icon(Constants.SPRITE_PLAYER_SHIP_32x32)
        pygame.display.set_caption("PewPew")
        pygame.display.init()
        pygame.joystick.init()
        pygame.font.init()

        # flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL | pygame.FULLSCREEN
        self.flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL

        self.is_fullscreen = False

        self.get_res = pygame.display.Info()
        self.resolution = Axis(
            x=int(self.get_res.current_w * 0.7), y=int(self.get_res.current_h * 0.7))
        self.screen = pygame.display.set_mode(
            self.resolution.to_list(), self.flags)
        pygame.display.set_caption("PewPew")

        pygame.mixer.music.set_volume(Constants.BGM_VOLUME)
        pygame.mixer.music.load(Constants.BGM_INDIGO)
        pygame.mixer.music.play(-1)

        self.state = Constants.RUNNING
        self.clock = pygame.time.Clock()
        self.render_frame_time = 0

        self.joysticks = []

        self.time_stop = False
        self.game_over = False

        self.bg = Background()
        self.bullet_manager = BulletManager()
        self.enemy_manager = EnemyManager()
        self.player_manager = PlayerManager()
        self.item_manager = ItemManager()

        self.fps = FPS()
        self.score = Score()

        self.player_manager.add(Player(x=self.resolution.x / 2, y=self.resolution.y / 2,
                                       speed=Presets.PLAYER_DEFAULT_SPEED,
                                       sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_BALANCE, 0.6).convert_alpha(),
                                       health=Presets.PLAYER_DEFAULT_HEALTH,
                                       weapon=Presets.PLAYER_DEFAULT_WEAPON,
                                       ))
        self.player_manager.add(Player(x=self.resolution.x / 2, y=self.resolution.y / 2,
                                       speed=Presets.PLAYER_DEFAULT_SPEED,
                                       sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_PIERCE, 0.6).convert_alpha(),
                                       health=Presets.PLAYER_DEFAULT_HEALTH,
                                       weapon=Presets.PLAYER_DEFAULT_WEAPON,

                                       ))
        self.player_manager.add(Player(x=self.resolution.x / 2, y=self.resolution.y / 2,
                                       speed=Presets.PLAYER_DEFAULT_SPEED,
                                       sprite=Utils.scale_image(
                                           Constants.SPRITE_PLAYER_SHIP_BALANCE, 0.6).convert_alpha(),
                                       health=Presets.PLAYER_DEFAULT_HEALTH,
                                       weapon=Presets.PLAYER_DEFAULT_WEAPON,

                                       ))

        # self.trail = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)

    def tick_clock(self):
        self.render_frame_time = self.clock.tick() / 10

    def start(self):

        while True:
            self.tick_clock()
            self.game_events()

            self.bg.render_background(self.screen, self.resolution)

            if self.state == Constants.RUNNING:
                normal_frame_time = self.render_frame_time
                if self.time_stop:
                    self.render_frame_time = 0.01

                self.bg.manage_stars(self.render_frame_time)

                for bullet in self.bullet_manager.bullets:
                    self.bullet_manager.move_bullet(bullet, self.render_frame_time),
                    self.bullet_manager.check_bullet(bullet, self.resolution),

                    bullet.render(self.screen)

                    for player in self.player_manager.players:
                        self.bullet_manager.has_collided(bullet, player,
                                                         lambda bullet: player.take_damage(bullet.damage),
                                                         use_hitbox=True
                                                         )

                for enemy in self.enemy_manager.enemies:
                    self.enemy_manager.move_enemy(enemy, self.render_frame_time)
                    self.enemy_manager.check_enemy(enemy, self.resolution)
                    self.bullet_manager.has_collided_any(enemy,
                                                         lambda bullet: enemy.take_damage(bullet.damage),
                                                         lambda bullet: self.score.add(173)
                                                         )
                    self.enemy_manager.check_death(enemy,
                                                   lambda item: self.item_manager.create_item(enemy.x, enemy.y))
                    for player in self.player_manager.players:
                        self.enemy_manager.has_collided(enemy, player,
                                                        lambda enemy: player.take_damage(player.max_health * 0.15),
                                                        lambda enemy: self.enemy_manager.enemies.remove(enemy)
                                                        )

                    enemy.shoot(self.bullet_manager) if self.time_stop is False else None
                    enemy.render(self.screen)

                # Items
                for item in self.item_manager.items:
                    for player in self.player_manager.players:
                        self.item_manager.has_collided(item, player,
                                                       lambda item: self.item_manager.items.remove(item))

                    item.render(self.screen)

                if self.render_frame_time != 0.01:
                    self.enemy_manager.spawn_enemy_random(self.resolution)

                self.render_frame_time = normal_frame_time

            elif self.state == Constants.PAUSE:
                pause_text = pygame.font.SysFont('Consolas', 40).render(
                    'Pause', True, pygame.color.Color('Red'))
                self.screen.blit(pause_text, (100, 100))

            if self.game_over:
                death_text = pygame.font.SysFont('Consolas', 40).render('U died', True, pygame.color.Color('White'))
                continue_text = pygame.font.SysFont('Consolas', 40).render('Press R to continue', True,
                                                                           pygame.color.Color('White'))
                self.screen.blit(death_text, (self.resolution.x / 2.2, 150))
                self.screen.blit(continue_text, (self.resolution.x / 3, 240))
            else:
                self.player_manager.render(self.screen)

            # self.trail.fill((255, 255, 255, 200), special_flags=pygame.BLEND_RGBA_MULT)
            # self.screen.blit(self.trail, (0, 0))

            self.fps.render(display=self.screen, fps=self.clock.get_fps(), position=Axis(self.resolution.x, 0))
            self.score.render(display=self.screen, position=Axis(0, 0))

            pygame.display.update()

    def game_events(self):
        self.check_game_over()

        if self.player_manager.is_alive() and self.state == Constants.RUNNING:
            for index, player in enumerate(self.player_manager.players):
                if len(self.joysticks) >= index + 1:
                    joy = self.joysticks[index]
                    player.layout = Presets.CONTROLLER_LAYOUT
                    player.control_ship_joystick(joy, self.render_frame_time,
                                                 limit=Axis(self.resolution.x - 1, self.resolution.y - 1))
                    player.control_shoot_joystick(joy, self.bullet_manager)
                    player.control_ultimate_joystick(joy, self.time_stop is False,
                                                     action=lambda: self.activate_time_stop(True))

                else:
                    keys = pygame.key.get_pressed()
                    player.layout = Presets.KEYBOARD_LAYOUTS[index - len(self.joysticks) - 1]
                    player.control_ship(keys, self.render_frame_time,
                                        limit=Axis(self.resolution.x - 1, self.resolution.y - 1))
                    player.control_shoot(keys, self.bullet_manager)
                    player.control_ultimate(keys, self.time_stop is False, action=lambda: self.activate_time_stop(True))

        for event in pygame.event.get():
            self.update_controller_state()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()

                if event.key == pygame.K_ESCAPE:
                    if self.state == Constants.PAUSE:
                        self.state = Constants.RUNNING
                    else:
                        self.state = Constants.PAUSE

                if event.key == pygame.K_RETURN:
                    if event.mod & pygame.KMOD_ALT:
                        self.fullscreen_mode()

            if event.type == Constants.ULTIMATE_END:
                self.activate_time_stop(False)

            if event.type == pygame.QUIT:
                pygame.quit()

    def check_game_over(self):
        if not self.player_manager.is_alive() and self.game_over is False:
            Constants.SFX_DEATH.play()
            self.game_over = True

    def activate_time_stop(self, activate):
        if activate:
            Constants.SFX_TIME_STOP.play()
            self.bg.color = [code + 50 for code in self.bg.color]
            self.time_stop = True
            pygame.time.set_timer(Constants.ULTIMATE_END, 5000)

        else:
            self.bg.color = Constants.BACKGROUND_COLOR
            self.time_stop = False

    def update_controller_state(self):
        joy_count = pygame.joystick.get_count()
        if joy_count != len(self.joysticks):
            self.joysticks = []
            for index in range(0, joy_count):
                self.joysticks.append(pygame.joystick.Joystick(index))
                self.joysticks[index].init()

    def reset_game(self):
        self.enemy_manager.reset()
        self.bullet_manager.reset()
        self.player_manager.reset()
        self.item_manager.reset()
        self.score.reset()
        self.game_over = False

    def fullscreen_mode(self):
        if self.is_fullscreen:
            self.resolution = Axis(x=int(self.get_res.current_w * 0.75),
                                   y=int(self.get_res.current_h * 0.75))
            self.flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL
        else:
            self.resolution = Axis(x=int(self.get_res.current_w),
                                   y=int(self.get_res.current_h))
            self.flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL | pygame.FULLSCREEN

        self.screen = pygame.display.set_mode(
            self.resolution.to_list(), self.flags)
        self.is_fullscreen = not self.is_fullscreen
