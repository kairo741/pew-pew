import pygame
from lib.manager.UltimateManager import UltimateManager
from lib.object.Axis import Axis
from lib.object.Background import Background
from lib.object.CustomJoy import CustomJoy
from lib.object.Text import Text
from lib.utils.Constants import Constants
from lib.utils.LayoutPresets import LayoutPresets


class GameManager:
    def __init__(self):
        super().__init__()
        pygame.display.set_icon(Constants.SPRITE_PLAYER_SHIP_32x32)
        pygame.display.set_caption("PewPew 🚀🛸")
        pygame.display.init()
        pygame.joystick.init()
        pygame.font.init()
        pygame.event.set_allowed([pygame.KEYDOWN, pygame.QUIT, Constants.ULTIMATE_END])

        self.base_flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.HWACCEL
        self.flags = self.base_flags

        self.is_fullscreen = False

        self.get_res = pygame.display.Info()
        self.resolution = Axis(
            x=int(self.get_res.current_w),
            y=int(self.get_res.current_h * 0.925))
        self.screen = pygame.display.set_mode(
            size=self.resolution.to_list(),
            flags=self.flags,
            depth=24)
        from .BulletManager import BulletManager
        from .EnemyManager import EnemyManager
        from .ItemManager import ItemManager
        from .NumberManager import NumberManager
        from .PauseManager import PauseManager
        from .PlayerManager import PlayerManager

        self.state = Constants.RUNNING
        self.clock = pygame.time.Clock()
        self.render_frame_time = 0

        self.joysticks = []

        self.time_stop = False
        self.game_over = False
        self.player_count = 4

        self.bg = Background()
        self.bullet_manager = BulletManager()
        self.enemy_manager = EnemyManager()
        self.player_manager = PlayerManager(time_stop_ultimate=self.activate_time_stop, bullet_manager=self.bullet_manager)
        self.number_manager = NumberManager()
        self.item_manager = ItemManager(self.number_manager)
        self.ultimate_manager = UltimateManager(background=self.bg)

        self.fps = Text(x=self.resolution.x)
        self.score = Text(x=0)

        self.player_manager.create_players(self.player_count, self.resolution)

        self.use_gyro = False

        if self.use_gyro:
            import hid
            self.joy_hid = hid.device()
            self.joy_hid.open(1356, 1476)
            self.joy_hid.set_nonblocking(1)

        self.sfx_sound_channel = pygame.mixer.Channel(Constants.SFX_MIXER_CHANNEL)
        self.bgm_sound_channel = pygame.mixer.Channel(Constants.BGM_MIXER_CHANNEL)
        self.sfx_sound_channel.set_volume(0)
        self.sfx_sound_channel.pause()
        self.bgm_sound_channel.set_volume(0)
        self.bgm_sound_channel.pause()
        self.bgm_sound_channel.play(pygame.mixer.Sound(Constants.BGM_INDIGO), -1)
        self.is_sound_paused = True
        self.pause = PauseManager(self)

    def tick_clock(self):
        self.render_frame_time = self.clock.tick() / 10

    def start(self):
        while True:
            self.tick_clock()
            self.game_events()

            self.bg.render_background(self.screen, self.resolution)

            if not self.game_over:
                self.player_manager.render(self.screen, self.render_frame_time)

            if self.state == Constants.RUNNING:
                normal_frame_time = self.render_frame_time
                if self.time_stop:
                    self.render_frame_time = 0.01

                self.bg.manage_stars(self.render_frame_time)

                self.manage_game_over()

                self.manage_bullets()
                self.manage_enemies()
                self.manage_items()

                if self.render_frame_time != 0.01:
                    self.enemy_manager.spawn_enemy_random(self.resolution, len(self.player_manager.players))

                self.render_frame_time = normal_frame_time


            self.fps.set_text(round(self.clock.get_fps()))
            self.fps.render(self.screen, align="top-right")
            
            self.score.render(self.screen, align="top-left")
            self.number_manager.render(self.screen, self.render_frame_time)

            if self.state == Constants.PAUSE:
                self.manage_game_over()
                self.pause.manage_pause()
            pygame.display.update()

    def game_events(self):
        self.check_game_over()
        self.player_input()
        self.update_controller_state()

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()

                if event.key == pygame.K_ESCAPE:
                    if self.state == Constants.PAUSE:
                        self.state = Constants.RUNNING
                    else:
                        self.state = Constants.PAUSE

                if event.key == pygame.K_RETURN:
                    if event.mod & pygame.KMOD_ALT:
                        self.fullscreen_mode()

                if event.key == pygame.K_F8:
                    if self.is_sound_paused:
                        self.sfx_sound_channel.set_volume(Constants.SFX_VOLUME)
                        self.sfx_sound_channel.unpause()
                        self.bgm_sound_channel.set_volume(Constants.BGM_VOLUME)
                        self.bgm_sound_channel.unpause()
                    else:
                        self.sfx_sound_channel.set_volume(0)
                        self.sfx_sound_channel.pause()
                        self.bgm_sound_channel.set_volume(0)
                        self.bgm_sound_channel.pause()
                    self.is_sound_paused = not self.is_sound_paused

                self.reset_keys(event.key)

            if event.type == pygame.JOYBUTTONDOWN and event.button == 6:
                if self.state == Constants.PAUSE:
                    self.state = Constants.RUNNING
                else:
                    self.state = Constants.PAUSE

            if event.type == Constants.ULTIMATE_END:
                self.ultimate_manager.disable_ultimate()

            if event.type == pygame.QUIT:
                pygame.quit()

    def player_input(self):
        if self.player_manager.is_alive() and self.state == Constants.RUNNING:
            for index, player in enumerate(self.player_manager.players):
                if len(self.joysticks) >= index + 1:
                    joy = self.joysticks[index]
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
                                                 limit=Axis(self.resolution.x - 1, self.resolution.y - 1))
                    player.control_shoot_joystick(joy, self.bullet_manager)
                    player.control_ultimate_joystick(joy,
                                                     action=lambda: self.ultimate_manager.do_ultimate(player.ultimate))

                else:
                    keys = pygame.key.get_pressed()
                    player.layout = LayoutPresets.KEYBOARD_LAYOUTS[index - len(self.joysticks)]
                    player.control_ship(keys, self.render_frame_time,
                                        limit=Axis(self.resolution.x - 1, self.resolution.y - 1))
                    player.control_shoot(keys, self.bullet_manager)
                    player.control_ultimate(keys, action=lambda: self.ultimate_manager.do_ultimate(player.ultimate))

    def manage_game_over(self):
        if self.game_over:
            death_text = Text(font_size=40, text="You Died")
            death_text.set_pos(self.resolution.x / 2, self.resolution.y/6)

            continue_text = Text(font_size=40, text="Press R to try again")
            continue_text.set_pos(self.resolution.x / 2, self.resolution.y/3.5)

            death_text.render(self.screen, align="center")
            continue_text.render(self.screen, align="center")

    def manage_items(self):
        for item in self.item_manager.items:
            self.item_manager.move_item(item, self.render_frame_time)
            self.item_manager.check_item(item, self.resolution)
            for player in self.player_manager.players:
                self.item_manager.has_collided(item, player,
                                               lambda item: self.item_manager.items.remove(item),
                                               lambda effect: item.effect(player), )

            item.render(self.screen)

    def manage_enemies(self):
        for enemy in self.enemy_manager.enemies:
            self.enemy_manager.move_enemy(enemy, self.render_frame_time)
            self.enemy_manager.check_enemy(enemy, self.resolution)
            self.bullet_manager.has_collided_any(enemy,
                                                 lambda bullet: enemy.take_damage(bullet.damage),
                                                 lambda bullet: self.score.add(173),
                                                 lambda bullet: self.number_manager.add_damage_number(bullet.x,
                                                                                                      bullet.y,
                                                                                                      bullet.damage))

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
            enemy.render(self.screen)

    def manage_bullets(self):
        for bullet in self.bullet_manager.bullets:
            self.bullet_manager.move_bullet(bullet, self.render_frame_time),
            self.bullet_manager.check_bullet(bullet, self.resolution),

            bullet.render(self.screen)

            for player in self.player_manager.players:
                self.bullet_manager.has_collided(bullet, player,
                                                 lambda bullet: player.take_damage(bullet.damage),
                                                 lambda bullet: self.number_manager.add_take_damage_number(bullet.x,
                                                                                                           bullet.y,
                                                                                                           bullet.damage))

    def check_game_over(self):
        if not self.player_manager.is_alive() and self.game_over is False:
            self.sfx_sound_channel.play(Constants.SFX_DEATH)
            self.game_over = True

    def activate_time_stop(self, activate):
        if activate:
            self.sfx_sound_channel.play(Constants.SFX_TIME_STOP)
            self.time_stop = True

        else:
            self.time_stop = False

    def update_controller_state(self):
        joy_count = pygame.joystick.get_count()
        if joy_count != len(self.joysticks):
            self.joysticks = []
            for index in range(0, joy_count):
                self.joysticks.append(pygame.joystick.Joystick(index))
                self.joysticks[index].init()

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
        self.score.reset()
        self.activate_time_stop(False)
        self.game_over = False
        self.player_manager.create_players(self.player_count, self.resolution)

    def fullscreen_mode(self):
        if self.is_fullscreen:
            self.resolution = Axis(x=int(self.get_res.current_w),
                                   y=int(self.get_res.current_h * 0.925))
            self.flags = self.base_flags
        else:
            self.resolution = Axis(x=int(self.get_res.current_w),
                                   y=int(self.get_res.current_h))
            self.flags = self.base_flags | pygame.FULLSCREEN

        self.screen = pygame.display.set_mode(self.resolution.to_list(), self.flags)
        self.is_fullscreen = not self.is_fullscreen
