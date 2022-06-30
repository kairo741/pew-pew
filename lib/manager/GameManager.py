import pygame

from .BulletManager import BulletManager
from .EnemyManager import EnemyManager
from object.Background import Background
from object.Axis import Axis
from object.Fps import FPS
from object.Ship import Ship
from utils.Constants import Constants
from utils.Utils import Utils


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

        self.joystick = None
        self.controller_connected = False

        self.bg = Background()
        self.bullet_manager = BulletManager()
        self.enemy_manager = EnemyManager()

        self.player = Ship(x=self.resolution.x / 2, y=self.resolution.y / 2, speed=Constants.PLAYER_DEFAULT_SPEED,
                           sprite=Utils.scale_image(
                               Constants.SPRITE_PLAYER_SHIP, 0.6).convert_alpha(),
                           health=Constants.PLAYER_DEFAULT_HEALTH,
                           weapon=Constants.PLAYER_DEFAULT_WEAPON, )

        self.player.set_size_with_sprite()

        self.time_stop = False
        self.game_over = False

    def tick_clock(self):
        self.render_frame_time = self.clock.tick() / 10

    def start(self):

        fps = FPS()

        while True:
            self.tick_clock()
            self.game_events()

            self.bg.render_background(self.screen, self.resolution)

            if self.state == Constants.RUNNING:
                normal_frame_time = self.render_frame_time
                if self.time_stop:
                    self.render_frame_time = 0.01

                self.bg.manage_stars(self.render_frame_time)

                self.bullet_manager.manage_bullets(
                    lambda bullet: self.bullet_manager.move_bullet(bullet, self.render_frame_time),
                    lambda bullet: self.bullet_manager.check_bullet(bullet, self.resolution), 
                    lambda bullet: bullet.render(self.screen)
                )

                self.enemy_manager.manage_enemies(
                    lambda enemy: self.enemy_manager.move_enemy(enemy, self.render_frame_time),
                    lambda enemy: self.enemy_manager.check_enemy(enemy, self.resolution),
                    lambda enemy: enemy.render(self.screen),
                    lambda enemy: self.bullet_manager.has_collided(enemy, lambda bullet: enemy.take_damage(bullet.damage)),
                    lambda enemy: self.enemy_manager.has_collided(enemy, self.player, 
                        lambda enemy: self.player.take_damage(self.player.max_health * 0.15),
                        lambda enemy: self.enemy_manager.enemies.remove(enemy))
                )
            
                if self.render_frame_time != 0.01:
                    self.enemy_manager.spawn_enemy_random(self.resolution)

                self.render_frame_time = normal_frame_time

            elif self.state == Constants.PAUSE:
                pause_text = pygame.font.SysFont('Consolas', 40).render(
                    'Pause', True, pygame.color.Color('Red'))
                self.screen.blit(pause_text, (100, 100))

            if self.game_over:
                death_text = pygame.font.SysFont('Consolas', 40).render('U died', True, pygame.color.Color('White'))
                continue_text = pygame.font.SysFont('Consolas', 40).render('Press R to continue', True, pygame.color.Color('White'))
                self.screen.blit(death_text, (self.resolution.x / 2.2, 150))
                self.screen.blit(continue_text, (self.resolution.x / 3, 240))
                self.player.disable()
            else:
                self.player.render(self.screen, is_player=True)

            fps.render(display=self.screen, fps=self.clock.get_fps(),
                       position=(self.resolution.x - 40, 0))
            pygame.display.update()

    def game_events(self):
        self.check_game_over()

        keys = pygame.key.get_pressed()
        if self.player.health > 0 and self.state == Constants.RUNNING:
            if keys[pygame.K_d]:
                if self.player.x + self.player.size.x < self.resolution.x - 1:
                    self.player.x += self.player.speed.x * self.render_frame_time

            if keys[pygame.K_a]:
                if self.player.x > 2:
                    self.player.x -= self.player.speed.x * self.render_frame_time

            if keys[pygame.K_w]:
                if self.player.y > 2:
                    self.player.y -= self.player.speed.y * self.render_frame_time

            if keys[pygame.K_s]:
                if self.player.y + self.player.size.y < self.resolution.y - 1:
                    self.player.y += self.player.speed.y * self.render_frame_time

            if keys[pygame.K_SPACE]:
                if pygame.time.get_ticks() - self.player.last_bullet > self.player.weapon.shoot_delay:

                    for generated_bullet in self.player.weapon.make_bullets(self.player.get_middle()):
                        self.bullet_manager.shoot(generated_bullet)

                    Constants.SFX_LASER.play()

                    self.player.last_bullet = pygame.time.get_ticks()

            if keys[pygame.K_x] and self.time_stop is False:
                self.activate_time_stop(True)

            if self.controller_connected:
                axis = Axis(self.joystick.get_axis(0),
                            self.joystick.get_axis(1))

                if axis.x > 0.2:
                    if self.player.x + self.player.size.x < self.resolution.x - 1:
                        self.player.x += self.player.speed.x * self.render_frame_time

                if axis.x < -0.2:
                    if self.player.x > 2:
                        self.player.x -= self.player.speed.x * self.render_frame_time

                if axis.y < 0.2:
                    if self.player.y > 2:
                        self.player.y -= self.player.speed.y * self.render_frame_time

                if axis.y > -0.2:
                    if self.player.y + self.player.size.y < self.resolution.y - 1:
                        self.player.y += self.player.speed.y * self.render_frame_time

                if self.joystick.get_button(2):
                    if pygame.time.get_ticks() - self.player.last_bullet > self.player.weapon.shoot_delay:

                        for generated_bullet in self.player.weapon.make_bullets(self.player.get_middle()):
                            self.bullet_manager.shoot(generated_bullet)

                        Constants.SFX_LASER.play()

                        self.player.last_bullet = pygame.time.get_ticks()

                if self.joystick.get_button(10) and self.time_stop is False:
                    self.activate_time_stop(True)

        for event in pygame.event.get():
            self.controller_state(pygame.joystick.get_count() > 0)
            if event.type == pygame.JOYBUTTONDOWN:
                if self.joystick.get_button(6):
                    if self.state == Constants.PAUSE:
                        self.state = Constants.RUNNING
                    else:
                        self.state = Constants.PAUSE

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
        if self.player.is_dead() and self.game_over is False:
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

    def controller_state(self, enabled):
        if enabled:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.controller_connected = True
        else:
            self.joystick = None
            self.controller_connected = False

    def reset_game(self):
        self.enemy_manager.reset()
        self.bullet_manager.reset()
        self.player.reset()
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
