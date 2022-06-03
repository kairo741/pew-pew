import pygame
from os import path
from object.GameObject import GameObject
from object.Size import Size


def mainLoop():

    pygame.display.init()

    flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL | pygame.FULLSCREEN
    flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL

    get_res = pygame.display.Info()
    resolution = Size(x=int(get_res.current_w*0.75),
                      y=int(get_res.current_h * 0.75),)
    screen = pygame.display.set_mode([resolution.x, resolution.y], flags)
    root = path.abspath(path.join(path.dirname(__file__), '..', ''))
    pygame.display.set_caption("PewPew")
    clock = pygame.time.Clock()
    center = [resolution.x // 2, resolution.y // 2]

    bg = GameObject(x=0, y=0, size=Size(resolution.x, resolution.y))

    player = GameObject(x=center[0], y=center[1],
                        size=Size(resolution.x*0.1, resolution.x*0.1),
                        sprite=pygame.image.load(
        root+"\\assets\\images\\ship.png").convert_alpha())

    bulletSprite = pygame.image.load(root+"\\assets\\images\\bullet.png").convert_alpha()
    bulletSprite = pygame.transform.scale(
        bulletSprite, (10, 50))

    player.sprite = pygame.transform.scale(
        player.sprite, (player.size.x, player.size.y))

    bullets = []

    lastBullet = 0

    while(True):
        timePassed = clock.tick(60) / 10

        pygame.draw.rect(screen, (50, 50, 50), bg.toRect())

        for bullet in bullets:
            screen.blit(bulletSprite, bullet.toRect())
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
            if (pygame.time.get_ticks() - lastBullet > 150):
                
                bullets.append(GameObject(x=player.x-5+player.size.x/2, y=player.y, size=Size(10, 50), sprite=bulletSprite))
                lastBullet = pygame.time.get_ticks()

        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_SPACE):
                    bullets.append(GameObject(
                        player.x-5+player.size.x/2, player.y, Size(10, 40)))

            if (event.type == pygame.QUIT):
                pygame.quit()

        print(clock.get_fps(), end='\r')


mainLoop()
