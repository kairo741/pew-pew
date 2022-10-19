from random import uniform

import pygame
from lib.Engine import Engine
from lib.manager.UltimateManager import UltimateManager
from lib.object.game.Axis import Axis
from lib.object.structure.CustomJoy import CustomJoy
from lib.object.structure.Sound import Sound
from lib.object.visual.Background import Background
from lib.object.visual.Score import Score
from lib.object.visual.Text import Text
from lib.utils.Constants import Constants
from lib.utils.LayoutPresets import LayoutPresets


class GameScreen:
    def __init__(self, engine=Engine()):
        self.engine = engine

        from lib.manager.BulletManager import BulletManager
        from lib.manager.EnemyManager import EnemyManager
        from lib.manager.ItemManager import ItemManager
        from lib.manager.NumberManager import NumberManager
        from lib.manager.PlayerManager import PlayerManager
        from lib.screen.PauseScreen import PauseScreen

        self.state = Constants.RUNNING
        self.time_stop = False
        self.game_over = False
        self.round_started = False
        self.player_count = 4

        self.bg = Background()
        self.bullet_manager = BulletManager()
        self.enemy_manager = EnemyManager()
        self.player_manager = PlayerManager(time_stop_ultimate=self.activate_time_stop,
                                            bullet_manager=self.bullet_manager)
        self.number_manager = NumberManager()
        self.item_manager = ItemManager(self.number_manager)
        self.ultimate_manager = UltimateManager(background=self.bg)

        self.pause = PauseScreen(self)

        self.fps = Text(x=self.engine.resolution.x)
        self.start_text = Text(x=self.engine.resolution.x/2, y=self.engine.resolution.y, text="Press Enter to Start")
        self.score = Score(x=0, text="Score: 0")

        self.player_manager.create_players(self.player_count, self.engine.resolution)

        self.use_gyro = False

        if self.use_gyro:
            import hid
            self.joy_hid = hid.device()
            self.joy_hid.open(1356, 1476)
            self.joy_hid.set_nonblocking(1)

        self.sound = Sound()
        self.sound.play_bg_music()
        self.sound.mute()

    def tick_clock(self):
        self.render_frame_time = self.engine.clock.tick() / 10

    def start(self):
        while True:
            self.tick_clock()
            self.game_events()

            if self.state == Constants.RUNNING:
                self.manage_game()

            elif self.state == Constants.PAUSE:
                self.manage_game_over()
                self.pause.manage_pause()

            if self.sound.is_sound_paused:
                self.sound.render_muted_icon(self.engine.screen, self.engine.resolution)

            self.engine.real_screen.blit(self.engine.screen, self.engine.screen_pos.to_list())
            pygame.display.update()

    def manage_game(self):
        self.bg.render_background(self.engine.screen, self.engine.resolution)

        if not self.game_over:
            self.player_manager.render(self.engine.screen, self.render_frame_time)

        normal_frame_time = self.render_frame_time
        if self.time_stop:
            self.render_frame_time = 0.01

        self.bg.manage_stars(self.render_frame_time)

        self.manage_game_over()

        self.manage_bullets()
        self.manage_enemies()
        self.manage_items()

        if self.round_started:
            if self.render_frame_time != 0.01:
                self.enemy_manager.spawn_enemy_random(self.engine.resolution, len(self.player_manager.players))

        else:
            self.start_text.render(self.engine.screen, align="bottom-center")

        self.render_frame_time = normal_frame_time

        self.fps.set_text(round(self.engine.clock.get_fps()))
        self.fps.render(self.engine.screen, align="top-right")

        self.score.render(self.engine.screen, align="top-left")
        self.number_manager.render(self.engine.screen, self.render_frame_time)

    def toggle_sound(self):
        if self.sound.is_sound_paused:
            self.sound.unmute()
        else:
            self.sound.mute()

    def game_events(self):
        self.check_game_over()
        self.player_input()
        self.update_controller_state()

        if self.ultimate_manager.get_shake_enabled():
            self.shake_screen(3)

        elif set(self.engine.screen_pos.to_list()) != set((0, 0)):
            self.engine.screen_pos = Axis(0, 0)

        for event in pygame.event.get():
            if self.state == Constants.PAUSE:
                self.pause.check_pause_events(event)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()

                if event.key == pygame.K_ESCAPE:
                    if self.state == Constants.PAUSE:
                        self.pause.stop_pause()
                        self.state = Constants.RUNNING
                    else:
                        self.pause.start_pause()
                        self.state = Constants.PAUSE

                if event.key == pygame.K_RETURN:
                    if event.mod & pygame.KMOD_ALT:
                        self.engine.fullscreen_mode()

                    elif not self.round_started:
                        self.round_started = True

                if event.key == pygame.K_F8:
                    self.toggle_sound()

                self.reset_keys(event.key)

            if event.type == pygame.JOYBUTTONDOWN and event.button == 6:
                if self.state == Constants.PAUSE:
                    self.pause.stop_pause()
                    self.state = Constants.RUNNING
                else:
                    self.pause.start_pause()
                    self.state = Constants.PAUSE

            if event.type == Constants.ULTIMATE_END:
                self.ultimate_manager.disable_ultimate()

            if event.type == pygame.QUIT:
                pygame.quit()

    def shake_screen(self, value):
        value *= (self.engine.resolution.x / 1000)
        self.engine.screen_pos = Axis(uniform(-value, value), uniform(-value, value))

    def player_input(self):
        if self.player_manager.is_alive() and self.state == Constants.RUNNING:
            for index, player in enumerate(self.player_manager.players):
                if len(self.engine.joysticks) >= index + 1:
                    joy = self.engine.joysticks[index]
                    control_joy = joy

                    player.layout = LayoutPresets.CONTROLLER_LAYOUT
                    joy_name = joy.get_name().lower()

                    if "xbox" in joy_name:
                        player.layout = LayoutPresets.XBOX_CONTROLLER_LAYOUT

                    if self.use_gyro and "sony" in joy_name or "ps" in joy_name:
                        try:
                            data = self.joy_hid.read(64)
                            control_joy = CustomJoy(data)
                        except:
                            pass

                    player.control_ship_joystick(control_joy, self.render_frame_time,
                                                 limit=Axis(self.engine.resolution.x - 1, self.engine.resolution.y - 1))
                    player.control_shoot_joystick(joy, self.bullet_manager)
                    player.control_ultimate_joystick(joy,
                                                     action=lambda: self.ultimate_manager.do_ultimate(player.ultimate))

                else:
                    keys = pygame.key.get_pressed()
                    player.layout = LayoutPresets.KEYBOARD_LAYOUTS[index - len(self.engine.joysticks)]
                    player.control_ship(keys, self.render_frame_time,
                                        limit=Axis(self.engine.resolution.x - 1, self.engine.resolution.y - 1))
                    player.control_shoot(keys, self.bullet_manager)
                    player.control_ultimate(keys, action=lambda: self.ultimate_manager.do_ultimate(player.ultimate))

    def manage_game_over(self):
        if self.game_over:
            death_text = Text(font_size=40, text="You Died")
            death_text.set_pos(self.engine.resolution.x / 2, self.engine.resolution.y / 6)

            continue_text = Text(font_size=40, text="Press R to try again")
            continue_text.set_pos(self.engine.resolution.x / 2, self.engine.resolution.y / 3.5)

            death_text.render(self.engine.screen, align="center")
            continue_text.render(self.engine.screen, align="center")

    def manage_items(self):
        for item in self.item_manager.items:
            self.item_manager.move_item(item, self.render_frame_time)
            self.item_manager.check_item(item, self.engine.resolution)
            for player in self.player_manager.players:
                self.item_manager.has_collided(item, player,
                                               lambda item: self.item_manager.items.remove(item),
                                               lambda effect: item.effect(player), )

            item.render(self.engine.screen)

    def manage_enemies(self):
        for enemy in self.enemy_manager.enemies:
            self.enemy_manager.move_enemy(enemy, self.render_frame_time)
            self.enemy_manager.check_enemy(enemy, self.engine.resolution)
            self.bullet_manager.has_collided_any(enemy,
                                                 lambda bullet: enemy.take_damage(bullet.damage),
                                                 lambda bullet: self.score.add(173),
                                                 lambda bullet: self.number_manager.add_damage_number(bullet.x,
                                                                                                      bullet.y,
                                                                                                      bullet.damage,
                                                                                                      bullet.is_crit))

            self.enemy_manager.check_death(enemy,
                                           lambda item: self.item_manager.random_item(enemy.x, enemy.y))
            for player in self.player_manager.players:
                self.enemy_manager.has_collided_player(enemy, player,
                                                       lambda enemy: player.take_damage(player.max_health * 0.33),
                                                       lambda enemy: self.number_manager.add_take_damage_number(enemy.x,
                                                                                                                enemy.y,
                                                                                                                player.max_health * 0.33),
                                                       render_frame_time=self.render_frame_time
                                                       )

            enemy.shoot(self.bullet_manager) if self.time_stop is False else None
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

    def check_game_over(self):
        if not self.player_manager.is_alive() and self.game_over is False:
            self.sound.sound_channel_sfx.play(Constants.SFX_DEATH)
            self.game_over = True

    def activate_time_stop(self, activate):
        if activate:
            self.sound.sound_channel_sfx.play(Constants.SFX_TIME_STOP)
            self.time_stop = True

        else:
            self.time_stop = False

    def update_controller_state(self):
        joy_count = pygame.joystick.get_count()
        if joy_count != len(self.engine.joysticks):
            self.engine.joysticks = []
            for index in range(0, joy_count):
                self.engine.joysticks.append(pygame.joystick.Joystick(index))
                self.engine.joysticks[index].init()

    def reset_keys(self, key):
        if key == pygame.K_F1 or key == pygame.K_F2 or key == pygame.K_F3 or key == pygame.K_F4 or key == pygame.K_F5:
            if key == pygame.K_F1:
                self.player_count = 1

            if key == pygame.K_F2:
                self.player_count = 2

            if key == pygame.K_F3:
                self.player_count = 3

            if key == pygame.K_F4:
                self.player_count = 4

            self.reset_game()

    def reset_game(self):
        self.ultimate_manager.reset()
        self.enemy_manager.reset()
        self.bullet_manager.reset()
        self.player_manager.reset()
        self.item_manager.reset()
        self.score.reset("Score: 0")
        self.activate_time_stop(False)
        self.game_over = False
        self.round_started = False
        self.player_manager.create_players(self.player_count, self.engine.resolution)

    def toggle_fullscreen(self):
        self.engine.fullscreen_mode()
        self.pause.copy_current_frame()
