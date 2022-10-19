from random import randint

from lib.object.players.PlayerBalance import PlayerBalance
from lib.object.players.PlayerFroggers import PlayerFroggers
from lib.object.players.PlayerHealer import PlayerHealer
from lib.object.players.PlayerVampire import PlayerVampire
from lib.utils.Presets import Presets
from lib.utils.Utils import Utils


class PlayerManager:
    def __init__(self, time_stop_ultimate, bullet_manager):
        self.time_stop_ultimate = time_stop_ultimate
        self.bullet_manager = bullet_manager
        self.players = []

    def add(self, player):
        player.sprite = Utils.scale_image(player.sprite, 0.6)
        player.set_size_with_sprite()
        self.players.append(player)

    def disable(self):
        for player in self.players:
            player.disable()

    def render(self, screen, render_frame_time, hide_hud=False):
        for player in self.players:
            player.player_passive(render_frame_time)
            player.render(screen, render_frame_time, hide_hud=hide_hud)

    def is_alive(self):
        for player in self.players:
            if player.health > 0:
                return True
        return False

    def reset(self):
        for player in self.players:
            player.reset()

    def set_spawn_position(self, resolution):
        players_len = len(self.players)
        base_pos = resolution.x / players_len + 1
        for index, player in enumerate(self.players):
            player.x = base_pos * (index + 0.5)
            player.initial_position.x = base_pos * (index + 0.5)


    def create_menu_player(self, resolution):
        self.players = []
        player_list_position = randint(0, len(Presets.PLAYER_LIST) - 1)
        self.create_player(resolution, Presets.PLAYER_LIST[player_list_position])

        self.show_players_dps()
        player = self.players[0]
        player.x -= player.size.x/2
        player.y = resolution.y/1.2
        self.players[0].weapon.weapon_type="single"


    def create_players(self, quantity, resolution):
        self.players = []
        for i in range(0, quantity):
            player_list_position = randint(0, len(Presets.PLAYER_LIST) - 1)
            self.create_player(resolution, Presets.PLAYER_LIST[player_list_position])

        self.show_players_dps()
        self.set_spawn_position(resolution)

    def show_players_dps(self):
        for i, player in enumerate(self.players):
            print(f'\033[1mP{i + 1} DPS:\033[0m '
                  f'\033[93m\033[4m{self.players[i].weapon.calculate_dps()}\033[0m')

    def create_player(self, resolution, player_preset):
        this_player = player_preset.copy()
        this_player.x = resolution.x
        this_player.y = resolution.y / 2
        this_player.weapon.source_reference = this_player

        if type(this_player) == PlayerBalance:
            this_player.time_stop = self.time_stop_ultimate

        if type(this_player) == PlayerHealer:
            this_player.team = self.players

        if type(this_player) == PlayerFroggers:
            this_player.bullet_manager = self.bullet_manager

        if type(this_player) == PlayerVampire:
            this_player.bullet_manager = self.bullet_manager

        self.add(this_player)

        self.set_spawn_position(resolution)
