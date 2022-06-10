from copy import copy
from os import path
from random import randint
from Utils.Constants import Constants

import pygame
from controller.BulletController import BulletController
from object.Fps import FPS
from object.GameObject import GameObject
from object.Background import Background
from object.Player import Player
from object.Axis import Axis


def scaleImage(image, scale):
    return pygame.transform.smoothscale(image, (image.get_width() * scale, image.get_height() * scale))


def mainLoop():
    pygame.display.init()
    pygame.mixer.init()
    pygame.font.init()

    flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL | pygame.FULLSCREEN
    flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL

    get_res = pygame.display.Info()
    resolution = Axis(x=int(get_res.current_w * 0.75),
                      y=int(get_res.current_h * 0.75))
    screen = pygame.display.set_mode([resolution.x, resolution.y], flags)
    root = Constants.ROOT_PATH
    pygame.display.set_caption("PewPew")
    clock = pygame.time.Clock()

    bg = Background(speed=Axis(0, 8), sprite=pygame.image.load(root + "\\assets\\images\\background.png"))
    bg.sprite = pygame.transform.smoothscale(bg.sprite, [resolution.x, resolution.y])
    bg.setSizeWithSprite()

    player = Player(x=resolution.x / 2, y=resolution.y / 2, speed=Axis(10, 7),
                    sprite=pygame.image.load(root + "\\assets\\images\\ship.png").convert_alpha())
    player.sprite = scaleImage(player.sprite, 0.5)
    player.setSizeWithSprite()

    bulletSprite = pygame.image.load(root + "\\assets\\images\\bullet.png").convert_alpha()
    bulletSprite = scaleImage(bulletSprite, 0.2)
    bullet_controller = BulletController()

    lastBullet = 0

    lastEnemy = 0

    enemySprite = pygame.image.load(root + "\\assets\\images\\shipEnemy.png").convert_alpha()
    enemySprite = scaleImage(enemySprite, 0.5)
    enemies = []

    fps = FPS()

    explosion_sfx = pygame.mixer.Sound(root + "\\assets\\sfx\\Explosion.mp3")
    explosion_sfx.set_volume(0.2)

    while (True):
        timePassed = clock.tick(60) / 10

        bg.render(screen)

        fps.render(display=screen, fps=clock.get_fps(), position=(resolution.x - 30, 0))
        bullet_controller.render_bullets(screen)


        for e in enemies:
            bullet_controller.has_collided(e, lambda: enemies.remove(e) )


        player.render(screen)

        if (pygame.time.get_ticks() - lastEnemy > 800):
            newEnemy = GameObject(x=resolution.x / 2, y=0, sprite=pygame.Surface.copy(enemySprite),
                                  speed=Axis(randint(-8, 8), randint(0, 4)))
            newEnemy.setSizeWithSprite()
            newEnemy.center()
            enemies.append(newEnemy)
            lastEnemy = pygame.time.get_ticks()

        for e in enemies:
            e.x += e.speed.x
            e.y += e.speed.y
            e.render((screen))

        pygame.display.update()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            if (player.x + player.size.x < resolution.x - 1):
                player.x += player.speed.x * timePassed

        if keys[pygame.K_a]:
            if player.x > 2:
                player.x -= player.speed.x * timePassed

        if (keys[pygame.K_w]):
            if (player.y > 2):
                player.y -= player.speed.y * timePassed

        if (keys[pygame.K_s]):
            if (player.y + player.size.y < resolution.y - 1):
                player.y += player.speed.y * timePassed

        if (keys[pygame.K_SPACE]):
            if (pygame.time.get_ticks() - lastBullet > 200):
                newBullet = GameObject(speed=Axis(0, -20), sprite=pygame.Surface.copy(bulletSprite))
                newBullet.setSizeWithSprite()
                newBullet.x = player.getMiddle().x - newBullet.getMiddle().x + 12
                newBullet.y = player.y
                bullet_controller.shoot(newBullet)

                newBullet = None
                newBullet = GameObject(speed=Axis(0, -20), sprite=pygame.Surface.copy(bulletSprite))
                newBullet.setSizeWithSprite()
                newBullet.x = player.getMiddle().x - newBullet.getMiddle().x - 12
                newBullet.y = player.y
                bullet_controller.shoot(newBullet)
                lastBullet = pygame.time.get_ticks()


        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    # TODO - modo tela cheia
                    DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.RESIZABLE)


mainLoop()
