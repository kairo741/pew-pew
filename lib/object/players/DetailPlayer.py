from lib.object.game.Axis import Axis
from lib.object.players.Player import Player
from lib.object.visual.Bar import Bar
from lib.object.visual.Text import Text
from lib.utils.Utils import Utils

from pygame import draw, transform


class DetailPlayer:
    def __init__(self, player: Player, x=0, y=0, index=0, resolution=Axis.zero(), name="", passive="", ultimate=""):
        self.index = index
        self.x = x
        self.y = y
        self.resolution = resolution

        self.name = Text(text=name, font_size=42)
        
        self.sprite = Utils.scale_image_raw(player.sprite, 3.5)
        self.small_sprite = Utils.scale_image_raw(player.sprite, 0.7)

        sprite_size = self.sprite.get_size()
        sprite_size = Axis(sprite_size[0], sprite_size[1])

        bar_x = x+sprite_size.x*1.7
        bar_space = self.resolution.y*0.07

        self.power = Bar(bar_x, y + bar_space*0, title="Power", value=player.weapon.bullet.damage, max_value=75, bar_width=self.resolution.x*0.1)
        self.health = Bar(bar_x, y + bar_space*1, title="Health", value=player.health, max_value=150, bar_width=self.resolution.x*0.1)   
        self.speed = Bar(bar_x, y + bar_space*2, title="Speed", value=player.speed.x + player.speed.y, max_value=14.4, bar_width=self.resolution.x*0.1)
        self.rate = Bar(bar_x, y + bar_space*3, title="Fire Rate", value=70/player.weapon.shoot_delay, max_value=1, bar_width=self.resolution.x*0.1)
        
        self.shoot_type = player.weapon.weapon_type
        self.passive_description = Text(text=passive, font_size=32)
        self.ultimate_description = Text(text=ultimate, font_size=32)


    def render(self, screen):
        size = self.sprite.get_size()
        text_surf = transform.rotate(self.name.get_surface(), 90)
        text_size = text_surf.get_size()

        draw.rect(screen, (255, 255, 255), (self.x, self.y, text_size[0], size[1]), width=1)
        screen.blit(text_surf, (self.x, self.y+(size[1] - text_size[1]) / 2))
        
        rect = [self.x+text_size[0], self.y, size[0], size[1]]
        screen.blit(self.sprite, rect)
        draw.rect(screen, (255, 255, 255), rect, width=1)

    def render_description(self, screen):
        self.passive_description.render(screen, align="top-left")
        self.ultimate_description.redner(screen, align="top-left")

    def render_stats(self, screen):
        self.power.render(screen)
        self.health.render(screen)
        self.speed.render(screen)
        self.rate.render(screen)


    def render_icon(self, screen, x, y):
        screen.blit(self.small_sprite, [x, y])


