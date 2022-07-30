from random import randint
from lib.utils.Constants import Constants
import pygame


class CRT:
    def __init__(self, screen, current_width, current_height):
        self.screen = screen
        self.tv = Constants.CRT_TV.convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (current_width, current_height))

    def create_crt_lines(self):
        line_height = 3
        line_amount = int(self.screen.get_height() / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (self.screen.get_width(), y_pos), 1)

    def draw(self):
        self.tv.set_alpha(randint(75, 90))
        self.create_crt_lines()
        self.screen.blit(self.tv, (0, 0))
