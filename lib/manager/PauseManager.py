from functools import partial
from lib.object.Axis import Axis
from lib.object.Button import Button
from lib.object.Crt import CRT
from lib.object.Text import Text
from pygame import K_DOWN, K_RETURN, K_UP, KEYDOWN, MOUSEBUTTONDOWN, K_s, K_w, Rect, quit, mouse, transform

from lib.utils.Presets import Presets
from lib.utils.Utils import Utils


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

        self.apply_change = False
        self.mouse_button_state = False

        self.players = []

        self.apply_button = None
        self.buttons = []

    def change_player(self, index, button_ref):
        self.mouse_button_state = False
        current_index = self.players[index]["index"]

        if current_index < len(Presets.PLAYER_LIST)-1:
            self.players[index]["index"] += 1
        else:
            self.players[index]["index"] = 0

        next_player = Presets.PLAYER_LIST[self.players[index]["index"]]
        button_ref.content = transform.smoothscale(next_player.sprite, button_ref.content.get_size())
        self.players[index]["player"] = next_player


    def set_apply_change(self):
        self.mouse_button_state = False
        self.apply_change = True


    def start_pause(self):
        self.apply_change = False
        self.mouse_button_state = False

        self.apply_button = None
        
        self.players = []
        self.buttons = []

        text = Text(font_size=40, text="Apply", color="Red").get_surface()
        text_size = text.get_size()
        self.apply_button = Button(x=self.game.resolution.x/2-(text_size[0]*1.5)/2, y=self.game.resolution.y*0.8, size=Axis(text_size[0]*1.5, text_size[1]*1.5), content=text)
        self.apply_button.on_click = lambda: self.set_apply_change()

        for index, player in enumerate(self.game.player_manager.players):
            x = (self.game.resolution.x/5)*(index+1)
            y = self.game.resolution.y/1.5

            button = Button(x=x, y=y, size=Axis(100, 100), content=player.sprite)
            button.on_click = Utils.copy_function2(self.change_player)
            button.on_click = partial(button.on_click, self, index, button)
            self.buttons.append(button)
            self.players.append({"index": 0, "player": player})

    def stop_pause(self):
        if self.apply_change:
            self.game.player_manager.players = []
            for player in self.players:
                self.game.player_manager.create_player(self.game.resolution, Presets.PLAYER_LIST[player["index"]])


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
        self.draw_buttons()
        crt.draw()

    def draw_buttons(self):
        self.apply_button.render(self.game.screen)
        self.apply_button.cursor_pos = mouse.get_pos()
        self.apply_button.cursor_clicked = self.mouse_button_state
        
        for button in self.buttons:
            button.cursor_pos = mouse.get_pos()
            button.cursor_clicked = self.mouse_button_state
            button.render(self.game.screen)

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

        elif self.state == "Sound":
            self.game.toggle_sound()

    def check_pause_events(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.mouse_button_state = True
        
        if event.type == KEYDOWN:
            self.move_cursor(event.key)

            if event.key == K_RETURN:
                self.execute_current_action()
