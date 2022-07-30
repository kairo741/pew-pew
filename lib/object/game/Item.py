from .Axis import Axis
from lib.object.structure.GameObject import GameObject
from random import randint
from lib.utils.Constants import Constants
from lib.utils.Utils import Utils


def get_random_effect(item_manager):
    # move_speed = {"effect": item_manager.raise_move_speed, "sprite": Constants.SPRITE_POWER_UP_8}
    heal = {"effect": item_manager.heal, "sprite": Utils.scale_image(Constants.SPRITE_POWER_UP_HEAL)}
    atk_speed = {"effect": item_manager.raise_attack_speed, "sprite": Utils.scale_image(Constants.SPRITE_POWER_UP_SPEED)}
    atk_damage = {"effect": item_manager.raise_damage, "sprite": Utils.scale_image(Constants.SPRITE_POWER_UP_ATK)}
    change_weapon = {"effect": item_manager.change_weapon_type, "sprite": Utils.scale_image(Constants.SPRITE_POWER_UP_RANDOM)}
    recharge_ult = {"effect": item_manager.recharge_ultimage, "sprite": Utils.scale_image(Constants.SPRITE_POWER_UP_CHARGE_ULT)}
    crit_rate = {"effect": item_manager.raise_crit_rate, "sprite": Utils.scale_image(Constants.SPRITE_POWER_UP_CRIT_RATE)}

    # 1/5 = 20% de chance de spawndsa
    if randint(1, 5) == 1:
        return atk_speed

    # tem 80% de chance de chegar nesse if
    # tem 26% de chance total de spawn
    elif randint(1, 3) == 1:
        return atk_damage

    elif randint(1, 2) == 1:
        return crit_rate

    elif randint(1, 4) == 1:
        return recharge_ult

    elif randint(1, 10) == 1:
        return change_weapon

    # tem 54% de chance de chegar aqui
    else:
        return heal


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
