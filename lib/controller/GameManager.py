import pygame
from random import randint

from .BulletManager import BulletManager
from .EnemyManager import EnemyManager
from object.Background import Background
from object.Axis import Axis
from object.Fps import FPS
from object.GameObject import GameObject
from object.Ship import Ship
from object.Weapon import Weapon
from utils.Constants import Constants
from utils.Utils import Utils


class GameManager:
    def __init__(self):
        super().__init__()
        pygame.display.set_icon(Constants.SPRITE_PLAYER_SHIP_32x32)
        pygame.display.set_caption("PewPew")
        pygame.display.init()
        pygame.joystick.init()
        pygame.mixer.init()
        pygame.font.init()

        # flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL | pygame.FULLSCREEN
        self.flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL

        self.is_fullscreen = False

        self.get_res = pygame.display.Info()
        self.resolution = Axis(x=int(self.get_res.current_w * 0.7),
                               y=int(self.get_res.current_h * 0.7))
        self.screen = pygame.display.set_mode(
            [self.resolution.x, self.resolution.y], self.flags)
        self.state = Constants.RUNNING

        self.clock = pygame.time.Clock()
        self.render_frame_time = 0
        # self.joystick = pygame.joystick.Joystick(0)
        # self.joystick.init()
        self.bullet_controller = BulletManager()
        self.enemy_manager = EnemyManager()
        # self.last_enemy = 0

    def tick_clock(self):
        self.render_frame_time = self.clock.tick() / 10

    def start(self):
        bg = Background()

        player = Ship(x=self.resolution.x / 2, y=self.resolution.y / 2, speed=Constants.PLAYER_DEFAULT_SPEED,
                      sprite=Constants.SPRITE_PLAYER_SHIP.convert_alpha(),
                      health=Constants.PLAYER_DEFAULT_HEALTH,
                      weapon=Constants.PLAYER_DEFAULT_WEAPON)
        player.sprite = Utils.scale_image(player.sprite, 0.7)
        player.set_size_with_sprite()

        fps = FPS()

        # explosion_sfx = Constants.SFX_EXPLOSION
        # explosion_sfx.set_volume(0.2)

        while True:
            self.game_events(player=player)

            if self.state == Constants.RUNNING:
                self.bullet_controller.move_bullets(self.render_frame_time, self.resolution)
                self.enemy_manager.move_enemies(self.render_frame_time)
                self.tick_clock()
                bg.render_background(
                    self.screen, self.resolution, self.render_frame_time)

                fps.render(display=self.screen, fps=self.clock.get_fps(),
                           position=(self.resolution.x - 40, 0))
                self.bullet_controller.render_bullets(self.screen)

                self.enemy_manager.render_enemies(self.screen)
                self.enemy_manager.spawn_enemy(self.resolution.x / 2, 0)
                for e in self.enemy_manager.enemies:
                    self.bullet_controller.has_collided(
                        e, lambda bullet: e.take_damage(bullet.damage)
                    )

                self.enemy_manager.has_collided(player, lambda: player.take_damage(e.max_health * 0.15))

                if player.health <= 0:
                    death_text = pygame.font.SysFont('Consolas', 40).render('U died', True,
                                                                            pygame.color.Color('White'))
                    continue_text = pygame.font.SysFont('Consolas', 40).render('Press R to continue', True,
                                                                               pygame.color.Color('White'))
                    self.screen.blit(death_text, (self.resolution.x / 2.2, 150))
                    self.screen.blit(continue_text, (self.resolution.x / 3, 240))
                    player.x = 0  # todo - alterar método de tirar o player (mesmo que não renderizado)da tela
                    player.y = 0  # todo - alterar método de tirar o player (mesmo que não renderizado) da tela

                    # pygame.quit()
                else:
                    player.render(self.screen, is_player=True)

            elif self.state == Constants.PAUSE:
                pause_text = pygame.font.SysFont('Consolas', 40).render('Pause', True, pygame.color.Color('White'))
                self.screen.blit(pause_text, (100, 100))

            pygame.display.update()

    def game_events(self, player):
        keys = pygame.key.get_pressed()
        if player.health > 0:
            if keys[pygame.K_d]:
                if player.x + player.size.x < self.resolution.x - 1:
                    player.x += player.speed.x * self.render_frame_time

            if keys[pygame.K_a]:
                if player.x > 2:
                    player.x -= player.speed.x * self.render_frame_time

            if keys[pygame.K_w]:
                if player.y > 2:
                    player.y -= player.speed.y * self.render_frame_time

            if keys[pygame.K_s]:
                if player.y + player.size.y < self.resolution.y - 1:
                    player.y += player.speed.y * self.render_frame_time

            if keys[pygame.K_SPACE]:
                if pygame.time.get_ticks() - player.last_bullet > player.weapon.shoot_delay:

                    for generated_bullet in player.weapon.make_bullets(player.get_middle()):
                        self.bullet_controller.shoot(generated_bullet)
                    player.last_bullet = pygame.time.get_ticks()

        # axis = Axis(self.joystick.get_axis(0), self.joystick.get_axis(1))

        # if axis.x > 0.2:
        #     if player.x + player.size.x < self.resolution.x - 1:
        #         player.x += player.speed.x * self.render_frame_time

        # if axis.x < -0.2:
        #     if player.x > 2:
        #         player.x -= player.speed.x * self.render_frame_time

        # if axis.y < 0.2:
        #     if player.y > 2:
        #         player.y -= player.speed.y * self.render_frame_time

        # if axis.y > -0.2:
        #     if player.y + player.size.y < self.resolution.y - 1:
        #         player.y += player.speed.y * self.render_frame_time

        # if self.joystick.get_button(2):
        #     if pygame.time.get_ticks() - player.last_bullet > player.weapon.shoot_delay:

        #         for generated_bullet in player.weapon.make_bullets(player.getMiddle()):
        #             self.bullet_controller.shoot(generated_bullet)
        #         player.last_bullet = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if self.state == Constants.PAUSE:
                        self.state = Constants.RUNNING
                    else:
                        self.state = Constants.PAUSE

                if player.health <= 0 and event.key == pygame.K_r:
                    self.reset_game(player)

                if event.key == pygame.K_RETURN:
                    if event.mod & pygame.KMOD_ALT:
                        self.fullscreen_mode()

    def reset_game(self, player):
        self.enemy_manager.enemies = []
        player.health = Constants.PLAYER_DEFAULT_HEALTH
        player.speed = Constants.PLAYER_DEFAULT_SPEED
        player.weapon = Constants.PLAYER_DEFAULT_WEAPON
        player.x = self.resolution.x / 2
        player.y = self.resolution.y / 2

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
            [self.resolution.x, self.resolution.y], self.flags)
        self.is_fullscreen = not self.is_fullscreen
