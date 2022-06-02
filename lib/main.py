import pygame
from object.GameObject import GameObject
from object.Size import Size

def render():

    pygame.display.init()

    flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.FULLSCREEN
    flags = pygame.DOUBLEBUF | pygame.HWSURFACE

    get_res = pygame.display.Info()
    resolution = [int(get_res.current_w*0.75), int(get_res.current_h * 0.75)]
    screen = pygame.display.set_mode(resolution, flags)
    pygame.display.set_caption("PewPew")
    clock = pygame.time.Clock()
    center = [resolution[0] // 2, resolution[1] // 2]

    obj = GameObject(center[0], center[1], Size(
        resolution[0]/75, resolution[0]/75))

    pygame.key.set_repeat(1)

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

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, resolution[0], resolution[1]))
        pygame.draw.rect(screen, (255, 255, 255), obj.toRect())

        pygame.display.update()

        clock.tick(60)

render()
