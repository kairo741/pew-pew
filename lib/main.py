import pygame
from os import path
from object.GameObject import GameObject
from object.Size import Size


def render():

    pygame.display.init()

    flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN
    flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL

    get_res = pygame.display.Info()
    resolution = [int(get_res.current_w*0.75), int(get_res.current_h * 0.75)]
    screen = pygame.display.set_mode(resolution, flags)
    root = path.abspath(path.join(
        path.dirname(__file__), '..', ''))
    pygame.display.set_caption("PewPew")
    clock = pygame.time.Clock()
    center = [resolution[0] // 2, resolution[1] // 2]

    bg = GameObject(x=0, y=0, size=Size(resolution[0], resolution[1]),)

    obj = GameObject(x=center[0], y=center[1], size=Size(resolution[0]/75, resolution[0]/75),
                     sprite=pygame.image.load(root+"\\assets\\images\\ship.png").convert_alpha())

    pygame.key.set_repeat(16)

    while(True):
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_d]):
            obj.x += 10

        if (keys[pygame.K_a]):
            obj.x -= 10

        if (keys[pygame.K_w]):
            obj.y -= 7

        if (keys[pygame.K_s]):
            obj.y += 7

        if (pygame.event.wait().type == pygame.QUIT):
            exit()

        pygame.draw.rect(screen, (50, 50, 50), bg.toRect())
        screen.blit(obj.sprite, obj.toRect())

        pygame.display.update()

        clock.tick(60)


render()
