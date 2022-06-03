from copy import copy
from os import path

import pygame

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
    resolution = Size(x=int(get_res.current_w*0.75),
                      y=int(get_res.current_h * 0.75))
    screen = pygame.display.set_mode([resolution.x, resolution.y], flags)
    root = path.abspath(path.join(path.dirname(__file__), '..', ''))
    pygame.display.set_caption("PewPew")
    clock = pygame.time.Clock()

    bg = GameObject(x=0, y=0, sprite=pygame.image.load(root+"\\assets\\images\\background.png") )
    bg.sprite = pygame.transform.smoothscale(bg.sprite,[resolution.x , resolution.y])
    bg.setSizeWithSprite()
    
    
    
    bg2 = copy(bg)
    bg2.y = -resolution.y
    
    player = GameObject(x=resolution.x/2, y=resolution.y/2, sprite=pygame.image.load(root+"\\assets\\images\\ship.png").convert_alpha())
    player.sprite = scaleImage(player.sprite, 0.5)
    player.setSizeWithSprite()

    baseBullet = GameObject(x=0, y=0, sprite=pygame.image.load(root+"\\assets\\images\\bullet.png").convert_alpha())
    baseBullet.sprite = scaleImage(baseBullet.sprite, 0.2)
    baseBullet.setSizeWithSprite()

    bullets = []
    lastBullet = 0
    
    enemy = GameObject(x=500, y=0, sprite=pygame.image.load(root+"\\assets\\images\\shipEnemy.png").convert_alpha())
    enemy.sprite = scaleImage(enemy.sprite, 0.5)
    enemy.setSizeWithSprite()
    enemies = []
    enemies.append(enemy)
    while(True):
        timePassed = clock.tick(60) / 10
        
        screen.blit(bg.sprite, bg.toRect())
        screen.blit(bg2.sprite, bg2.toRect())
        
        bg.y+=8
        bg2.y+=8
        
        if(bg2.y > -1):
            bg2.y = -resolution.y
            bg.y = 0

        for bullet in bullets:
            screen.blit(bullet.sprite, bullet.toRect())
            bullet.y -= 20 * timePassed
            for e in enemies:
                if (bullet.toRect().colliderect(e.toRect())):
                    enemies.remove(e)
                

            if (bullet.y < -bullet.size.y):
                bullets.remove(bullet)

        screen.blit(player.sprite, player.toRect())
        
        for e in enemies:
            screen.blit(e.sprite, e.toRect())

        pygame.display.update()

        keys = pygame.key.get_pressed()

        if (keys[pygame.K_d]):
            if (player.x+player.size.x < resolution.x-1):
                player.x += 10 * timePassed

        if (keys[pygame.K_a]):
            if (player.x > 2):
                player.x -= 10 * timePassed

        if (keys[pygame.K_w]):
            if (player.y > 2):

                player.y -= 7 * timePassed

        if (keys[pygame.K_s]):
            if (player.y+player.size.y < resolution.y-1):

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
