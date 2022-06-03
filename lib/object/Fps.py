import pygame


class FPS:

    def __init__(self):
        self.font = pygame.font.SysFont("Verdana", 20)

    def render(self, display, fps, position):
        text = self.font.render(str(round(fps)), True, (255, 255, 255))
        display.blit(text, position)  # todo - deixar dinamico o position (está fazendo  position=(resolution.x-30, 0))
