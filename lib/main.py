from copy import copy
import pygame
from os import path
from object.GameObject import GameObject
from object.Size import Size


def scaleImage(image, scale):
    return pygame.transform.smoothscale(
        image, (image.get_width()*scale, image.get_height()*scale))


def mainLoop():

    pygame.display.init()

    flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL | pygame.FULLSCREEN
    flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL

    get_res = pygame.display.Info()
    resolution = Size(x=int(get_res.current_w*0.75), y=int(get_res.current_h * 0.75))
    screen = pygame.display.set_mode([resolution.x, resolution.y], flags)
    root = path.abspath(path.join(path.dirname(__file__), '..', ''))
    pygame.display.set_caption("PewPew")
    clock = pygame.time.Clock()

    bg = GameObject(x=0, y=0, size=Size(resolution.x, resolution.y))

    player = GameObject(x=resolution.x/2, y=resolution.y/2, sprite=pygame.image.load(root+"\\assets\\images\\ship.png").convert_alpha())
    player.sprite = scaleImage(player.sprite, 0.5)
    player.setSizeWithSprite()

    baseBullet = GameObject(x=0,y=0, sprite=pygame.image.load(root+"\\assets\\images\\bullet.png").convert_alpha())
    baseBullet.sprite = scaleImage(baseBullet.sprite, 0.2)
    baseBullet.setSizeWithSprite()

    bullets = []
    lastBullet = 0

    while(True):
        timePassed = clock.tick(60) / 10

        pygame.draw.rect(screen, (50, 50, 50), bg.toRect())

        for bullet in bullets:
            screen.blit(bullet.sprite, bullet.toRect())
            bullet.y -= 20 * timePassed

        screen.blit(player.sprite, player.toRect())

        pygame.display.update()

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_d]):
            player.x += 10 * timePassed

        if (keys[pygame.K_a]):
            player.x -= 10 * timePassed

        if (keys[pygame.K_w]):
            player.y -= 7 * timePassed

        if (keys[pygame.K_s]):
            player.y += 7 * timePassed

        if (keys[pygame.K_SPACE]):
            if (pygame.time.get_ticks() - lastBullet > 200):
                newBullet = copy(baseBullet)
                newBullet.x = player.getMiddle().x - newBullet.getMiddle().x+12
                newBullet.y = player.y
                bullets.append(newBullet)
                
                newBullet = copy(baseBullet)
                newBullet.x = player.getMiddle().x - newBullet.getMiddle().x-12
                newBullet.y = player.y
                bullets.append(newBullet)
                lastBullet = pygame.time.get_ticks()

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()

        print(clock.get_fps(), end='\r')


mainLoop()
