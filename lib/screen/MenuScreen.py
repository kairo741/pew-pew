from lib.object.game.MenuOption import MenuOption
from lib.screen.SelectScreen import SelectScreen
from lib.utils.Utils import Utils

import pygame
from lib.Engine import Engine
from lib.object.game.Axis import Axis
from lib.object.visual.Background import Background
from lib.object.visual.Text import Text
from lib.utils.Constants import Constants
from lib.utils.LayoutPresets import LayoutPresets


class MenuScreen:
    def __init__(self, engine: Engine):
        self.engine = engine

        from lib.manager.BulletManager import BulletManager
        from lib.manager.PlayerManager import PlayerManager

        self.bg = Background()
        self.bullet_manager = BulletManager()
        self.player_manager = PlayerManager(time_stop_ultimate=lambda: None,
                                            bullet_manager=self.bullet_manager)


        self.calculate_object_pos()
        self.credits = False
        self.intro_frames = []


    def calculate_object_pos(self):
        self.title = Text(x=self.engine.resolution.x/2, y=0, text="PEW PEW", font_size=96)
        title_rect = self.title.get_hitbox_rect()
        self.subtitle = Text(x=self.engine.resolution.x/2, y=title_rect[1]+title_rect[3]*1.5, text="THE GAME", font_size=24)

        self.player_manager.create_menu_player(self.engine.resolution)

        menu_space = self.engine.resolution.x/4

        self.menu_options = [
            MenuOption(self.engine.resolution.x/2 - menu_space, self.engine.resolution.y/2.5, function=self.goto_credits, sprite=Utils.scale_image(
                Constants.SPRITE_MENU_METEOR, 0.14).convert_alpha(), text=Text(text="Credits", font_size=42)
            ),
            MenuOption(self.engine.resolution.x/2, self.engine.resolution.y/2.5, function=self.goto_select, sprite=Utils.scale_image(
                Constants.SPRITE_MENU_METEOR, 0.2).convert_alpha(), text=Text(text="Play", font_size=42)
            ),
            MenuOption(self.engine.resolution.x/2 + menu_space, self.engine.resolution.y/2.5, function=pygame.quit, sprite=Utils.scale_image(
                Constants.SPRITE_MENU_METEOR, 0.14).convert_alpha(), text=Text(text="Exit", font_size=42)
            ),   
        ]
        self.back_option = MenuOption(self.engine.resolution.x/10, self.engine.resolution.x/10, function=self.goto_menu, sprite=Utils.scale_image(
                Constants.SPRITE_MENU_METEOR, 0.14).convert_alpha(), text=Text(text="Back", font_size=42)
            )

        self.options = self.menu_options

    def tick_clock(self):
        self.render_frame_time = self.engine.clock.tick() / 10


    def goto_select(self):
        SelectScreen(engine=self.engine, bg=self.bg).start()
        self.calculate_object_pos()

    def goto_menu(self):
        self.credits = False
        self.options = self.menu_options

    def goto_credits(self):
        self.credits = True
        self.options = [self.back_option]

    def run_intro(self):
        zoom = 5
        last_zoom = 0
        self.write_frame_intro(zoom)
        self.run_frame(custom_frame=self.intro_frames[0])
        while True:
            self.engine.check_quit_event_only()
            self.write_frame_intro(zoom)
            zoom -= round(0.45**zoom - (0.1**(zoom/2))*1.4, 2)

            if zoom == last_zoom:
                break
            last_zoom = zoom

            if zoom < 1:
                break

        print(f"wrote {len(self.intro_frames)} frames")
        
        for index, frame in enumerate(self.intro_frames):
            self.engine.check_quit_event_only()
            if index == int(len(self.intro_frames)*0.3):
                channel = pygame.mixer.Channel(Constants.MIXER_CHANNEL_EFFECTS)
                channel.play(Constants.SFX_START)

            self.run_frame(custom_frame=frame)


    def start(self, intro=True):
        if intro:
            self.run_intro()

        self.engine.sound.play_menu_music()

        while True:
            self.run_frame()

    
    def write_frame_intro(self, zoom):
        self.tick_clock()
        self.manage_game()

        self.render_title()

        zoom_screen = pygame.transform.scale(self.engine.screen, self.engine.resolution.scale_to(zoom).to_list())
        size = zoom_screen.get_size()
        pos = [
            -(size[0] - self.engine.resolution.x)/2, 
            -(size[1] - self.engine.resolution.y)/1.05
        ]
        self.intro_frames.append([zoom_screen, pos])


    def render_title(self):
        self.title.render(self.engine.screen, align="top-center")
        self.subtitle.render(self.engine.screen)

    def run_frame(self, custom_frame=None):    
        self.tick_clock()
        if not custom_frame:
            self.game_events()
            self.manage_game()

        self.render_title()

        if custom_frame:
            self.engine.real_screen.blit(custom_frame[0], custom_frame[1])
        else:
            self.engine.real_screen.blit(self.engine.screen, self.engine.screen_pos.to_list())

        pygame.display.update()

    
    def manage_options(self):
        for option in self.options:
            option.render(self.engine.screen, self.render_frame_time)

            for bullet in self.bullet_manager.bullets:
                if bullet.collided_with(option):
                    option.glow_scale *= 2
                    option.set_glow()

                    self.bullet_manager.reset()
                    self.run_frame()
                    option.function()

                    option.glow_scale = 2
                    option.set_glow()

    def manage_game(self):
        self.bg.render_background(self.engine.screen, self.engine.resolution)
        self.player_manager.render(self.engine.screen, self.render_frame_time, hide_hud=True)

        self.bg.manage_stars(self.render_frame_time)
        self.manage_bullets()
        self.manage_options()

    def game_events(self):
        self.player_input()
        self.update_controller_state()

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if event.mod & pygame.KMOD_ALT:
                        self.engine.fullscreen_mode()
                        self.calculate_object_pos()

                if event.key == pygame.K_F8:
                    self.engine.toggle_sound()

            if event.type == pygame.QUIT:
                pygame.quit()

    def player_input(self):
    
        for index, player in enumerate(self.player_manager.players):
            if len(self.engine.joysticks) >= index + 1:
                joy = self.engine.joysticks[index]
                control_joy = joy

                player.layout = LayoutPresets.CONTROLLER_LAYOUT
                joy_name = joy.get_name().lower()

                if "xbox" in joy_name:
                    player.layout = LayoutPresets.XBOX_CONTROLLER_LAYOUT

                player.control_ship_joystick(control_joy, self.render_frame_time,
                                                limit=Axis(self.engine.resolution.x - 1, self.engine.resolution.y - 1))
                player.control_shoot_joystick(joy, self.bullet_manager)
                player.control_ultimate_joystick(joy,
                                                    action=lambda: None)

            else:
                keys = pygame.key.get_pressed()
                player.layout = LayoutPresets.KEYBOARD_LAYOUTS[index - len(self.engine.joysticks)]
                player.control_ship(keys, self.render_frame_time,
                                    limit=Axis(self.engine.resolution.x - 1, self.engine.resolution.y - 1))
                player.control_shoot(keys, self.bullet_manager)
                player.control_ultimate(keys, action=lambda: None)
        

    def manage_bullets(self):
        for bullet in self.bullet_manager.bullets:
            self.bullet_manager.move_bullet(bullet, self.render_frame_time),
            self.bullet_manager.check_bullet(bullet, self.engine.resolution),

            bullet.render(self.engine.screen)

            for player in self.player_manager.players:
                self.bullet_manager.has_collided(bullet, player,
                                                 lambda bullet: player.take_damage(bullet.damage),
                                                 lambda bullet: self.number_manager.add_take_damage_number(bullet.x,
                                                                                                           bullet.y,
                                                                                                           bullet.damage))


    def update_controller_state(self):
        joy_count = pygame.joystick.get_count()
        if joy_count != len(self.engine.joysticks):
            self.engine.joysticks = []
            for index in range(0, joy_count):
                self.engine.joysticks.append(pygame.joystick.Joystick(index))
                self.engine.joysticks[index].init()
