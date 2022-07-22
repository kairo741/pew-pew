import pygame
from pygame import font
from lib.utils.Constants import Constants
from lib.object.Crt import CRT


class PauseManager:

    def __init__(self):
        self.font = font.Font(Constants.FONT_RETRO_GAMING, 40)

    def manage_pause(self, game):
        crt = CRT(game.screen, game.get_res.current_w, game.get_res.current_h)

        pause_text = self.font.render(
            'Pause', True, pygame.color.Color('Red'))
        for bullet in game.bullet_manager.bullets:
            bullet.render(game.screen)
        game.screen.blit(pause_text, (100, 100))
        for enemy in game.enemy_manager.enemies:
            enemy.render(game.screen)
        for item in game.item_manager.items:
            item.render(game.screen)
        crt.draw()
