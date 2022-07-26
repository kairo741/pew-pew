from random import randint
from lib.object.PlayerBalance import PlayerBalance
from lib.object.PlayerHealer import PlayerHealer
from lib.object.Ultimate import Ultimate

from lib.utils.Presets import Presets
from lib.utils.Utils import Utils


class PlayerManager:
    def __init__(self, time_stop_ultimate):
        self.time_stop_ultimate = time_stop_ultimate
        self.players = []

    def add(self, player):
        player.sprite = Utils.scale_image(player.sprite, 0.6)
        player.set_size_with_sprite()
        self.players.append(player)

    def disable(self):
        for player in self.players:
            player.disable()

    def render(self, screen, render_frame_time):
        for player in self.players:
            player.player_passive(render_frame_time)
            player.render(screen, render_frame_time)

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

    def create_players(self, quantity, resolution):
        self.players = []
        for i in range(0, quantity):
            player_list_position = randint(0, len(Presets.PLAYER_LIST) - 1)
            this_player = Presets.PLAYER_LIST[player_list_position].copy()
            this_player.x = resolution.x
            this_player.y = resolution.y / 2
            this_player.weapon.source_reference = this_player

            if type(this_player) == PlayerBalance:
                this_player.ultimate = Ultimate(lambda: self.time_stop_ultimate(True),
                                                lambda: self.time_stop_ultimate(False), duration=5)

            if type(this_player) == PlayerHealer:
                this_player.team = self.players

            self.add(this_player)

            print(f'\033[1mP{i + 1} DPS:\033[0m '
                  f'\033[93m\033[4m{self.players[i].weapon.calculate_dps()}\033[0m')

        self.set_spawn_position(resolution)
