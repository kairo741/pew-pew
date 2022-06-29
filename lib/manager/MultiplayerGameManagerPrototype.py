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


class MultiplayerGameManagerPrototype:
    def __init__(self):
        super().__init__()
        pygame.display.init()
        pygame.mixer.init()
        pygame.font.init()

        # flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL | pygame.FULLSCREEN
        self.flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL

        self.is_fullscreen = False

        self.get_res = pygame.display.Info()
        self.resolution = Axis(x=int(self.get_res.current_w * 0.9),
                               y=int(self.get_res.current_h * 0.9))
        self.screen = pygame.display.set_mode(
            [self.resolution.x, self.resolution.y], self.flags)

        pygame.display.set_caption("PewPew")
        self.clock = pygame.time.Clock()
        self.render_frame_time = 0

        self.bullet_manager = BulletManager()
        self.last_enemy = 0

    def tick_clock(self):
        self.render_frame_time = self.clock.tick() / 10

    def start(self):
        bg = Background()

        player_colors = [(255, 100, 100, 255), (100, 100, 255, 255)]

        players = [Ship(x=self.resolution.x / 2, y=self.resolution.y / 2, speed=Axis(10, 7),
                        sprite=Constants.SPRITE_PLAYER_SHIP.convert_alpha(),
                        weapon=Weapon(shoot_delay=300, weapon_type="triple",
                                      bullet_sprite=Utils.scale_image(Constants.SPRITE_BULLET, 0.2))),
                   Ship(x=self.resolution.x / 2, y=self.resolution.y / 2, speed=Axis(10, 7),
                        sprite=Constants.SPRITE_PLAYER_SHIP.convert_alpha(),
                        weapon=Weapon(shoot_delay=200, weapon_type="double",
                                      bullet_sprite=Utils.scale_image(Constants.SPRITE_BULLET, 0.2)), )]

        for i in range(0, len(players)):
            mask = pygame.Surface(Constants.SPRITE_PLAYER_SHIP.get_size())
            mask.fill(player_colors[i])
            players[i].sprite = Utils.scale_image(players[i].sprite, 0.5)
            players[i].set_size_with_sprite()
            players[i].sprite.blit(
                mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

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
            self.bullet_manager.render_bullets(self.screen)

            for e in enemies:
                self.bullet_manager.has_collided(
                    e, lambda bullet: e.take_damage(bullet.damage)
                )
                if (e.health < 0):
                    enemies.remove(e)

            for player in players:
                player.render(self.screen)

            if pygame.time.get_ticks() - self.last_enemy > 800:
                new_enemy = Ship(x=self.resolution.x / 2, y=0, sprite=pygame.Surface.copy(enemy_sprite),
                                 speed=Axis(randint(-2, 2), randint(0, 4)))
                new_enemy.set_size_with_sprite()
                new_enemy.center()
                enemies.append(new_enemy)
                self.last_enemy = pygame.time.get_ticks()

            for e in enemies:
                e.x += e.speed.x * self.render_frame_time
                e.y += e.speed.y * self.render_frame_time
                e.render(self.screen)

            pygame.display.update()
            self.game_events(players=players)

    def game_events(self, players):
        self.bullet_manager.move_bullets(self.render_frame_time, self.resolution)

        keys = pygame.key.get_pressed()

        for i in range(0, len(players)):
            player = players[i]
            if i == 0:

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
                    if pygame.time.get_ticks() - player.last_bullet > 200:
                        if pygame.time.get_ticks() - player.last_bullet > player.weapon.shoot_delay:

                            for generated_bullet in player.weapon.make_bullets(player.get_middle()):
                                self.bullet_manager.shoot(generated_bullet)
                            player.last_bullet = pygame.time.get_ticks()

            else:
                if keys[pygame.K_RIGHT]:
                    if player.x + player.size.x < self.resolution.x - 1:
                        player.x += player.speed.x * self.render_frame_time

                if keys[pygame.K_LEFT]:
                    if player.x > 2:
                        player.x -= player.speed.x * self.render_frame_time

                if keys[pygame.K_UP]:
                    if player.y > 2:
                        player.y -= player.speed.y * self.render_frame_time

                if keys[pygame.K_DOWN]:
                    if player.y + player.size.y < self.resolution.y - 1:
                        player.y += player.speed.y * self.render_frame_time

                if keys[pygame.K_RETURN]:
                    if pygame.time.get_ticks() - player.last_bullet > 200:
                        for generated_bullet in player.weapon.make_bullets(player.get_middle()):
                            self.bullet_manager.shoot(generated_bullet)
                            player.last_bullet = pygame.time.get_ticks()

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
