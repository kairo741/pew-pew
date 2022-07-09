
from object.Axis import Axis
from object.Layout import Layout
from object.Weapon import Weapon
from pygame import K_DOWN, K_LEFT, K_RETURN, K_RIGHT, K_RSHIFT, K_SPACE, K_UP, K_a, K_d, K_h, K_i, K_j, K_k, K_l, K_n, K_s, K_w, K_x

from utils.Constants import Constants
from utils.Utils import Utils


class Presets:
    # Player attributes
    PLAYER_DEFAULT_HEALTH = 100
    PLAYER_DEFAULT_SPEED = Axis(7, 5)
    PLAYER_BALANCE_WEAPON = Weapon(
        shoot_delay=125,
        weapon_type="triple",
        bullet_sprite=Utils.scale_image(Constants.SPRITE_BULLET_BLUE, 0.2),
        tag=Constants.TAG_PLAYER
    )

    PLAYER_PIERCE_WEAPON = Weapon(
        shoot_delay=300,
        weapon_type="single",
        bullet_sprite=Utils.scale_image(Constants.SPRITE_BULLET_LIGHTBLUE, 0.2),
        tag=Constants.TAG_PLAYER,
        pierce=True
    )

    PLAYER_FROG_WEAPON = Weapon(
        shoot_delay=200,
        weapon_type="spread",
        bullet_sprite=Utils.scale_image(Constants.SPRITE_BULLET_GREEN, 0.2),
        tag=Constants.TAG_PLAYER
    )

    PLAYER_SPEED_WEAPON = Weapon(
        shoot_delay=50,
        weapon_type="double",
        bullet_sprite=Utils.scale_image(Constants.SPRITE_BULLET_RED, 0.2),
        tag=Constants.TAG_PLAYER,
        damage=7
    )

    PRIMARY_KB_LAYOUT = Layout(K_w, K_s, K_a, K_d, K_SPACE, K_x)
    SECONDARY_KB_LAYOUT = Layout(K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RSHIFT, K_RETURN)
    EXTRA1_KB_LAYOUT = Layout(K_i, K_k, K_j, K_l, K_n, K_h)

    KEYBOARD_LAYOUTS = [PRIMARY_KB_LAYOUT, SECONDARY_KB_LAYOUT, EXTRA1_KB_LAYOUT, EXTRA1_KB_LAYOUT]

    CONTROLLER_LAYOUT = Layout(0.2, -0.2, 0.2, -0.2, 2, 10)
