from random import randint, uniform

from lib.object.Axis import Axis
from lib.object.Item import Item, get_random_effect
from lib.utils.Constants import Constants
from lib.utils.Utils import Utils


class ItemManager:
    def __init__(self, number_manager):
        super().__init__()
        self.items = []
        self.item_sprites = [Constants.POWER_UP_1, Constants.POWER_UP_2, Constants.POWER_UP_3, Constants.POWER_UP_4,
                             Constants.POWER_UP_5, Constants.POWER_UP_5, Constants.POWER_UP_6]
        self.number_manager = number_manager  # TODO - verificar se é a melhor maneira

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

    def check_item(self, item, screen_size):
        if item.y < -(item.size.y * 2):
            self.items.remove(item)
        elif item.x < -(item.size.x * 2):
            self.items.remove(item)
        elif item.x > screen_size.x:
            self.items.remove(item)
        elif item.y > screen_size.y:
            self.items.remove(item)

    def heal(self, player):
        heal_value = uniform(player.max_health * 0.05, player.max_health * 0.15)
        if player.health < player.max_health:
            if heal_value + player.health >= player.max_health:
                player.health = player.max_health
                text = 'MAX'
            else:
                player.health += heal_value
                text = f'+{round(heal_value)}'

            self.number_manager.add_heal_number(player.x,
                                                player.y, text)

    def raise_attack_speed(self, player):
        atk_speed = player.weapon.shoot_delay - uniform(0.2, 0.5)  # TODO - balancear valores
        if atk_speed > 0:
            player.weapon.shoot_delay = atk_speed
        else:
            player.weapon.shoot_delay = 0

        self.number_manager.add_buff_info(player.x, player.y, "+SPEED")

    def raise_damage(self, player):
        player.weapon.bullet.damage += uniform(1, 3)  # TODO - balancear valores
        self.number_manager.add_buff_info(player.x, player.y, "+ATK")

    def raise_move_speed(self, player):
        player.speed.x += uniform(0.7, 2.2)  # TODO - balancear valores
        player.speed.y += uniform(0.3, 1.5)  # TODO - balancear valores
