import pygame
from random import randint

from .BulletManager import BulletManager
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

        pygame.display.set_caption("PewPew")
        self.clock = pygame.time.Clock()
        self.render_frame_time = 0
        # self.joystick = pygame.joystick.Joystick(0)
        # self.joystick.init()

        self.bullet_controller = BulletManager()
        self.last_enemy = 0

    def tick_clock(self):
        self.render_frame_time = self.clock.tick() / 10

    def start(self):
        bg = Background()

        player = Ship(x=self.resolution.x / 2, y=self.resolution.y / 2, speed=Axis(10, 7),
                      sprite=Constants.SPRITE_PLAYER_SHIP.convert_alpha(),
                      weapon=Weapon(shoot_delay=100, weapon_type="triple",
                                    bullet_sprite=Utils.scale_image(Constants.SPRITE_BULLET, 0.2)))
        player.sprite = Utils.scale_image(player.sprite, 0.2)
        player.set_size_with_sprite()

        enemy_sprite = Utils.scale_image(Constants.SPRITE_ENEMY_SHIP, 0.5)
        enemies = []

        fps = FPS()

        # explosion_sfx = Constants.SFX_EXPLOSION
        # explosion_sfx.set_volume(0.2)

        while True:
            self.tick_clock()
            bg.render_background(
                self.screen, self.resolution, self.render_frame_time)

            fps.render(display=self.screen, fps=self.clock.get_fps(),
                       position=(self.resolution.x - 30, 0))
            self.bullet_controller.render_bullets(self.screen)

            for e in enemies:
                self.bullet_controller.has_collided(
                    e, lambda bullet: e.take_damage(bullet.damage)
                )
                if (e.collided_with(player, rect=player.get_hitbox_rect())):
                    player.take_damage(e.max_health * 0.15)
                    e.take_damage(e.health)

                if (e.health <= 0):
                    enemies.remove(e)

            if (player.health <= 0):
                pygame.quit()

            player.render(self.screen, is_player=True)

            if pygame.time.get_ticks() - self.last_enemy > 800:
                new_enemy = Ship(x=self.resolution.x / 2, y=0, sprite=pygame.Surface.copy(enemy_sprite),
                                 speed=Axis(Utils.random_int(-4, 4), randint(0, 4)))
                new_enemy.set_size_with_sprite()
                new_enemy.center()
                enemies.append(new_enemy)
                self.last_enemy = pygame.time.get_ticks()

            for e in enemies:
                e.x += e.speed.x * self.render_frame_time
                e.y += e.speed.y * self.render_frame_time
                e.render(self.screen)

            pygame.display.update()
            self.game_events(player=player)

    def game_events(self, player):
        self.bullet_controller.move_bullets(self.render_frame_time, self.resolution)

        keys = pygame.key.get_pressed()

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
                if event.key == pygame.K_RETURN:
                    if event.mod & pygame.KMOD_ALT:
                        self.fullscreen_mode()

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
