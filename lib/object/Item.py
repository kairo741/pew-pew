from .Axis import Axis
from .GameObject import GameObject
from random import choice
from lib.utils.Constants import Constants
from lib.utils.Utils import Utils


def get_random_effect(item_manager):
    heal = {"effect": item_manager.heal, "sprite": Constants.POWER_UP_6}
    atk_speed = {"effect": item_manager.raise_attack_speed, "sprite": Constants.POWER_UP_3}
    atk_damage = {"effect": item_manager.raise_damage, "sprite": Constants.POWER_UP_1}
    # move_speed = {"effect": item_manager.raise_move_speed, "sprite": Constants.POWER_UP_8}
    effects = [heal, atk_speed, heal, atk_damage, heal]  # TODO - fazer os IFs das chances de spawn
    return choice(effects)


class Item(GameObject):
    def __init__(
            self,
            x=0,
            y=0,
            size=Axis.zero(),
            speed=Axis.zero(),
            sprite="",
            effect=None):
        super().__init__(x, y, size, speed, sprite)
        self.effect = effect

    def render(self, screen):
        super().render(screen)
