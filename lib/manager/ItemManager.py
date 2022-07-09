from utils.Constants import Constants
from utils.Utils import Utils
from object.Item import Item
from pygame import Surface, time
from random import choice


class ItemManager:
    def __init__(self):
        super().__init__()
        self.items = []
        self.item_sprites = [Constants.POWER_UP_1, Constants.POWER_UP_2, Constants.POWER_UP_3, Constants.POWER_UP_4,
                             Constants.POWER_UP_5, Constants.POWER_UP_5, Constants.POWER_UP_6]

    def create_item(self, x, y):
        item_sprite = Utils.scale_image(choice(self.item_sprites), 0.5)
        new_item = Item(
            x=x,
            y=y,
            sprite=item_sprite,
        )
        new_item.set_size_with_sprite()
        new_item.center()
        self.items.append(new_item)
