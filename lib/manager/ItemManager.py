from utils.Constants import Constants
from utils.Utils import Utils
from object.Item import Item
from object.Axis import Axis
from random import randint, uniform
from random import choice


class ItemManager:
    def __init__(self):
        super().__init__()
        self.items = []
        self.item_sprites = [Constants.POWER_UP_1, Constants.POWER_UP_2, Constants.POWER_UP_3, Constants.POWER_UP_4,
                             Constants.POWER_UP_5, Constants.POWER_UP_5, Constants.POWER_UP_6]

    def reset(self):
        self.items = []

    def create_item(self, x, y):
        item_sprite = Utils.scale_image(choice(self.item_sprites), 0.3)
        new_item = Item(
            x=x,
            y=y,
            speed=Axis(uniform(-2, 2), randint(1, 3)),
            sprite=item_sprite,
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
