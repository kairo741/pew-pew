import pygame

from .BulletManager import BulletManager
from .EnemyManager import EnemyManager
from object.Background import Background
from object.Axis import Axis
from object.Fps import FPS
from object.Ship import Ship
from object.Weapon import Weapon
from utils.Constants import Constants
from utils.Utils import Utils


class GameManager:
    def __init__(self):
        super().__init__()
        pygame.display.set_icon(Constants.SPRITE_PLAYER_SHIP_32x32)
        pygame.display.init()
        pygame.joystick.init()
        pygame.mixer.init()
        pygame.font.init()

        # flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL | pygame.FULLSCREEN
        self.flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL

        self.is_fullscreen = False

        self.get_res = pygame.display.Info()
        self.resolution = Axis(x=int(self.get_res.current_w * 0.7), y=int(self.get_res.current_h * 0.7))
        self.screen = pygame.display.set_mode(self.resolution.to_list(), self.flags)
        pygame.display.set_caption("PewPew")

        self.clock = pygame.time.Clock()
        self.render_frame_time = 0
        
        self.joystick = None
        self.controller_connected = False

        self.bullet_manager = BulletManager()
        self.enemy_manager = EnemyManager()
        # self.last_enemy = 0

    def tick_clock(self):
        self.render_frame_time = self.clock.tick() / 10

    def start(self):
        bg = Background()

        player = Ship(x=self.resolution.x / 2, y=self.resolution.y / 2, speed=Axis(10, 7),
                      sprite=Constants.SPRITE_PLAYER_SHIP.convert_alpha(),
                      weapon=Weapon(shoot_delay=100, weapon_type="triple",
                                    bullet_sprite=Utils.scale_image(Constants.SPRITE_BULLET, 0.2)))
        player.sprite = Utils.scale_image(player.sprite, 0.7)
        player.set_size_with_sprite()

        fps = FPS()

        # explosion_sfx = Constants.SFX_EXPLOSION
        # explosion_sfx.set_volume(0.2)

        while True:
            self.tick_clock()
            bg.render_background(
                self.screen, self.resolution, self.render_frame_time)

            fps.render(display=self.screen, fps=self.clock.get_fps(),
                       position=(self.resolution.x - 40, 0))
            self.bullet_manager.render_bullets(self.screen)

            self.enemy_manager.render_enemies(self.screen)
            self.enemy_manager.spawn_enemy(self.resolution.x / 2, 0)
            for e in self.enemy_manager.enemies:
                self.bullet_manager.has_collided(
                    e, lambda bullet: e.take_damage(bullet.damage)
                )

            self.enemy_manager.has_collided(player, lambda: player.take_damage(e.max_health * 0.15))

            if (player.health <= 0):
                pygame.quit()

            player.render(self.screen, is_player=True)

            pygame.display.update()
            self.game_events(player=player)

    def game_events(self, player):
        self.bullet_manager.move_bullets(self.render_frame_time, self.resolution)
        self.enemy_manager.move_enemies(self.render_frame_time)

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
                    self.bullet_manager.shoot(generated_bullet)
                player.last_bullet = pygame.time.get_ticks()

        if self.controller_connected:
            axis = Axis(self.joystick.get_axis(0), self.joystick.get_axis(1))

            if axis.x > 0.2:
                if player.x + player.size.x < self.resolution.x - 1:
                    player.x += player.speed.x * self.render_frame_time

            if axis.x < -0.2:
                if player.x > 2:
                    player.x -= player.speed.x * self.render_frame_time

            if axis.y < 0.2:
                if player.y > 2:
                    player.y -= player.speed.y * self.render_frame_time

            if axis.y > -0.2:
                if player.y + player.size.y < self.resolution.y - 1:
                    player.y += player.speed.y * self.render_frame_time

            if self.joystick.get_button(2):
                if pygame.time.get_ticks() - player.last_bullet > player.weapon.shoot_delay:

                    for generated_bullet in player.weapon.make_bullets(player.get_middle()):
                        self.bullet_manager.shoot(generated_bullet)
                    player.last_bullet = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            self.controller_state(pygame.joystick.get_count() > 0)
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if event.mod & pygame.KMOD_ALT:
                        self.fullscreen_mode()

    def controller_state(self, enabled):
        if enabled:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.controller_connected = True
        else:
            self.joystick = None
            self.controller_connected = False

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
