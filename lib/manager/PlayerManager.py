class PlayerManager:
    def __init__(self):
        self.players = []

    def add(self, player):
        player.set_size_with_sprite()
        self.players.append(player)

    def disable(self):
        for player in self.players:
            player.disable()

    def render(self, screen):
        for player in self.players:
            player.render(screen)

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
