from random import uniform

import pygame
from lib.Engine import Engine
from lib.object.game.Axis import Axis
from lib.object.structure.Sound import Sound
from lib.object.visual.Background import Background
from lib.object.visual.Text import Text
from lib.utils.Constants import Constants
from lib.utils.LayoutPresets import LayoutPresets


class MenuScreen:
    def __init__(self):
        super().__init__()
        self.engine = Engine()

        from lib.manager.BulletManager import BulletManager
        from lib.manager.EnemyManager import EnemyManager
        from lib.manager.PlayerManager import PlayerManager

        self.bg = Background()
        self.bullet_manager = BulletManager()
        self.enemy_manager = EnemyManager()
        self.player_manager = PlayerManager(time_stop_ultimate=lambda: None,
                                            bullet_manager=self.bullet_manager)

        self.fps = Text(x=self.engine.resolution.x)
        self.start_text = Text(x=self.engine.resolution.x/2, y=self.engine.resolution.y, text="Press Enter to Start")

        self.player_manager.create_players(1, self.engine.resolution)

        self.sound = Sound()
        self.sound.play_bg_music()
        self.sound.mute()

    def tick_clock(self):
        self.render_frame_time = self.engine.clock.tick() / 10

    def start(self):
        while True:
            self.tick_clock()
            self.game_events()

            self.manage_game()

            self.engine.real_screen.blit(self.engine.screen, self.engine.screen_pos.to_list())
            pygame.display.update()

    def manage_game(self):
        self.bg.render_background(self.engine.screen, self.engine.resolution)
        self.player_manager.render(self.engine.screen, self.render_frame_time, hide_hud=True)

        self.bg.manage_stars(self.render_frame_time)
        self.manage_bullets()
        self.manage_enemies()

    def toggle_sound(self):
        if self.sound.is_sound_paused:
            self.sound.unmute()
        else:
            self.sound.mute()

    def game_events(self):
        self.player_input()
        self.update_controller_state()

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if event.mod & pygame.KMOD_ALT:
                        self.engine.fullscreen_mode()

                    elif not self.round_started:
                        self.round_started = True

                if event.key == pygame.K_F8:
                    self.toggle_sound()

            if event.type == pygame.QUIT:
                pygame.quit()

    def shake_screen(self, value):
        value *= (self.engine.resolution.x / 1000)
        self.engine.screen_pos = Axis(uniform(-value, value), uniform(-value, value))

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

    def manage_enemies(self):
        for enemy in self.enemy_manager.enemies:
            self.enemy_manager.move_enemy(enemy, self.render_frame_time)
            self.enemy_manager.check_enemy(enemy, self.engine.resolution)
            self.bullet_manager.has_collided_any(enemy,
                                                 lambda bullet: enemy.take_damage(bullet.damage),
                                                 lambda bullet: self.number_manager.add_damage_number(bullet.x,
                                                                                                      bullet.y,
                                                                                                      bullet.damage,
                                                                                                      bullet.is_crit))

            self.enemy_manager.check_death(enemy,
                                           lambda : None)

            enemy.render(self.engine.screen)

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

    def toggle_fullscreen(self):
        self.engine.fullscreen_mode()
        self.pause.copy_current_frame()
