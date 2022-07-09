from utils.Constants import Constants
from utils.Utils import Utils
from object.Item import Item, get_random_effect
from object.Axis import Axis
from random import randint, uniform, choice


class ItemManager:
    def __init__(self):
        super().__init__()
        self.items = []
        self.item_sprites = [Constants.POWER_UP_1, Constants.POWER_UP_2, Constants.POWER_UP_3, Constants.POWER_UP_4,
                             Constants.POWER_UP_5, Constants.POWER_UP_5, Constants.POWER_UP_6]

    def reset(self):
        self.items = []

    def random_item(self, x, y):
        if randint(1, 3) == 1:
            self.create_item(x, y)

    def create_item(self, x, y):
        effect = get_random_effect(self)
        new_item = Item(
            x=x,
            y=y,
            speed=Axis(uniform(-2, 2), randint(1, 3)),
            sprite=Utils.scale_image(effect['sprite'], 0.3),
            effect=effect['effect'],
        )
        new_item.set_size_with_sprite()
        new_item.center()
        self.items.append(new_item)

    def move_item(self, item, render_frame_time):
        item.x += item.speed.x * render_frame_time
        item.y += item.speed.y * render_frame_time

    def has_collided(self, item, object, *actions):
        if item.collided_with(object, object.get_hitbox_rect()):
            try:
                for action in actions:
                    action(item)
            except:
                print("error in item collision action")

    def heal(self, player):
        value = uniform(player.max_health*0.05, player.max_health*0.15)
        if player.health < player.max_health:
            if value + player.health > player.max_health:
                player.health = player.max_health
            else:
                player.health += value
