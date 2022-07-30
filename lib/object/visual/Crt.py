from random import randint
from lib.utils.Constants import Constants
import pygame


class CRT:
    def __init__(self, current_width, current_height):
        self.tv = Constants.CRT_TV.convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (current_width, current_height))

    def create_crt_lines(self, height, width):
        line_height = 3
        line_amount = int(height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (width, y_pos), 1)

    def draw(self, screen):

        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines(screen.get_height(), screen.get_width())
        screen.blit(self.tv, (0, 0))
