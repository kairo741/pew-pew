import pygame
from random import randint
from ..controller.BulletController import BulletController
from ..object.Fps import FPS
from ..object.GameObject import GameObject
from ..object.Background import Background
from ..object.Player import Player
from ..object.Axis import Axis
from ..Utils.Constants import Constants
from ..Utils.Utils import Utils


class GameController:
    def __init__(self):
        super().__init__()
        pygame.display.init()
        pygame.mixer.init()
        pygame.font.init()

        # flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL | pygame.FULLSCREEN
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL

        get_res = pygame.display.Info()
        self.resolution = Axis(x=int(get_res.current_w * 0.75),
                               y=int(get_res.current_h * 0.75))
        self.screen = pygame.display.set_mode([self.resolution.x, self.resolution.y], flags)

        pygame.display.set_caption("PewPew")
        self.clock = pygame.time.Clock()

        self.bullet_controller = BulletController()
        self.last_bullet = 0
        self.last_enemy = 0

    def start(self):
        root = Constants.ROOT_PATH
        bg = Background()
        bg.star_sprite = Utils.scale_image(Constants.SPRITE_STAR, 0.2)

        player = Player(x=self.resolution.x / 2, y=self.resolution.y / 2, speed=Axis(10, 7),
                        sprite=Constants.SPRITE_PLAYER_SHIP.convert_alpha())
        player.sprite = Utils.scale_image(player.sprite, 0.5)
        player.setSizeWithSprite()

        bullet_sprite = Utils.scale_image(Constants.SPRITE_BULLET, 0.2)
        bullet_controller = BulletController()


        enemy_sprite = Utils.scale_image(Constants.SPRITE_ENEMY_SHIP, 0.5)
        enemies = []

        fps = FPS()

        # explosion_sfx = Constants.SFX_EXPLOSION
        # explosion_sfx.set_volume(0.2)

        while True:

            bg.render_background(self.screen)

            fps.render(display=self.screen, fps=self.clock.get_fps(),
                       position=(self.resolution.x - 30, 0))
            bullet_controller.render_bullets(self.screen)

            for e in enemies:
                bullet_controller.has_collided(e, lambda: enemies.remove(e))

            player.render(self.screen)

            if pygame.time.get_ticks() - self.last_enemy > 800:
                new_enemy = GameObject(x=self.resolution.x / 2, y=0, sprite=pygame.Surface.copy(enemy_sprite),
                                       speed=Axis(randint(-8, 8), randint(0, 4)))
                new_enemy.setSizeWithSprite()
                new_enemy.center()
                enemies.append(new_enemy)
                self.last_enemy = pygame.time.get_ticks()

            for e in enemies:
                e.x += e.speed.x
                e.y += e.speed.y
                e.render(self.screen)

            self.game_events(player=player)

    def game_events(self, player):
        pygame.display.update()
        time_passed = self.clock.tick(60) / 10
        bullet_sprite = Utils.scale_image(Constants.SPRITE_BULLET.convert_alpha(), 0.2)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            if player.x + player.size.x < self.resolution.x - 1:
                player.x += player.speed.x * time_passed

        if keys[pygame.K_a]:
            if player.x > 2:
                player.x -= player.speed.x * time_passed

        if keys[pygame.K_w]:
            if player.y > 2:
                player.y -= player.speed.y * time_passed

        if keys[pygame.K_s]:
            if player.y + player.size.y < self.resolution.y - 1:
                player.y += player.speed.y * time_passed

        # TODO - arrumar balas
        if keys[pygame.K_SPACE]:
            if pygame.time.get_ticks() - self.last_bullet > 200:
                new_bullet = GameObject(speed=Axis(
                    0, -20), sprite=pygame.Surface.copy(bullet_sprite))
                new_bullet.setSizeWithSprite()
                new_bullet.x = player.getMiddle().x - new_bullet.getMiddle().x + 12
                new_bullet.y = player.y
                self.bullet_controller.shoot(new_bullet)

                new_bullet = None
                new_bullet = GameObject(speed=Axis(
                    0, -20), sprite=pygame.Surface.copy(bullet_sprite))
                new_bullet.setSizeWithSprite()
                new_bullet.x = player.getMiddle().x - new_bullet.getMiddle().x - 12
                new_bullet.y = player.y
                self.bullet_controller.shoot(new_bullet)
                self.last_bullet = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # TODO - modo tela cheia
                    DISPLAYSURF = pygame.display.set_mode(
                        (0, 0), pygame.RESIZABLE)
