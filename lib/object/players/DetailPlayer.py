from lib.object.players.Player import Player
from lib.object.visual.Text import Text
from lib.utils.Utils import Utils

from pygame import draw, transform


class DetailPlayer:
    def __init__(self, player: Player, x=0, y=0, index=0):
        self.index = index
        self.x = x
        self.y = y

        self.name = "Froggers"
        self.text = Text(text=self.name, font_size=42)
        
        self.sprite = Utils.scale_image_raw(player.sprite, 3)
        self.small_sprite = Utils.scale_image_raw(player.sprite, 0.7)
        self.power = player.weapon.bullet.damage
        self.health = player.health
        self.speed = player.speed.x + player.speed.y
        self.rate = player.weapon.shoot_delay
        
        self.shoot_type = None
        self.passive_description = ""
        self.ultimate_description = ""


    def render(self, screen):
        size = self.sprite.get_size()
        text_surf = transform.rotate(self.text.get_surface(), 90)
        text_size = text_surf.get_size()

        draw.rect(screen, (255, 255, 255), (self.x, self.y, text_size[0], size[1]), width=1)
        screen.blit(text_surf, (self.x, self.y+(size[1] - text_size[1]) / 2))
        
        rect = [self.x+text_size[0], self.y, size[0], size[1]]
        screen.blit(self.sprite, rect)
        draw.rect(screen, (255, 255, 255), rect, width=1)

    def render_icon(self, screen, x, y):
        screen.blit(self.small_sprite, [x, y])


