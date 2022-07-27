from lib.object.Axis import Axis
from lib.object.Crt import CRT
from lib.object.Text import Text
from pygame import K_DOWN, K_RETURN, K_UP, KEYDOWN, K_s, K_w, Rect, quit


class PauseManager:

    def __init__(self, game):
        self.cursor_rect = Rect(0, 0, 20, 20)
        self.game = game
        self.offset = - 100
        self.center_width = game.resolution.x / 2
        self.center_height = (game.resolution.y / 2) - 100

        self.state = 'Sound'
        self.sound_pos = Axis(self.center_width, self.center_height)
        self.teste_pos = Axis(self.center_width, self.center_height + 60)
        self.exit_pos = Axis(self.center_width, self.center_height + 120)
        self.cursor_rect.midtop = (self.center_width + self.offset, self.center_height)

    def manage_pause(self):
        crt = CRT(self.game.screen, self.game.resolution.x, self.game.resolution.y)
        pause_text = Text(text="Pause", color="Red", font_size=60, x=self.game.resolution.x/2, y=self.game.resolution.y/4)
        pause_text.render(self.game.screen, align="center")

        for bullet in self.game.bullet_manager.bullets:
            bullet.render(self.game.screen)
        for enemy in self.game.enemy_manager.enemies:
            enemy.render(self.game.screen)
        for item in self.game.item_manager.items:
            item.render(self.game.screen)

        self.display_pause_menu()
        self.update_center_pos()
        self.draw_cursor()
        crt.draw()

    def update_center_pos(self):
        self.center_width = self.game.resolution.x / 2
        self.center_height = (self.game.resolution.y / 2) - 100
        self.sound_pos = Axis(self.center_width, self.center_height)
        self.teste_pos = Axis(self.center_width, self.center_height + 60)
        self.exit_pos = Axis(self.center_width, self.center_height + 120)
        self.cursor_rect.x = self.sound_pos.x - 100

    def display_pause_menu(self):
        self.draw_text('Sound', self.sound_pos.x, self.sound_pos.y)
        self.draw_text('Teste', self.teste_pos.x, self.teste_pos.y)
        self.draw_text('Exit', self.exit_pos.x, self.exit_pos.y)

    def draw_text(self, txt, x, y):
        txt = Text(text=txt, x=x, y=y, font_size=40)
        txt.render(self.game.screen)

    def draw_cursor(self):
        self.draw_text('>', self.cursor_rect.x, self.cursor_rect.y)

    def move_cursor(self, key):
        if key == K_DOWN or key == K_s:
            if self.state == 'Sound':
                self.cursor_rect.midtop = (self.teste_pos.x + self.offset, self.teste_pos.y)
                self.state = 'Teste'
            elif self.state == 'Teste':
                self.cursor_rect.midtop = (self.exit_pos.x + self.offset, self.exit_pos.y)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.sound_pos.x + self.offset, self.sound_pos.y)
                self.state = 'Sound'
        elif key == K_UP or key == K_w:
            if self.state == 'Sound':
                self.cursor_rect.midtop = (self.exit_pos.x + self.offset, self.exit_pos.y)
                self.state = 'Exit'
            elif self.state == 'Exit':
                self.cursor_rect.midtop = (self.teste_pos.x + self.offset, self.teste_pos.y)
                self.state = 'Teste'
            elif self.state == 'Teste':
                self.cursor_rect.midtop = (self.sound_pos.x + self.offset, self.sound_pos.y)
                self.state = 'Sound'

    def execute_current_action(self):
        if self.state == "Exit":
            quit()

    def check_pause_events(self, event):
        if event.type == KEYDOWN:
            self.move_cursor(event.key)

            if event.key == K_RETURN:
                self.execute_current_action()
