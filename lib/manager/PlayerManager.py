

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

    
