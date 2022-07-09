
from object.Bullet import Bullet
from object.Axis import Axis
from object.Layout import Layout
from object.Weapon import Weapon
from pygame import K_DOWN, K_LEFT, K_RCTRL, K_RIGHT, K_RSHIFT, K_SPACE, K_UP, K_a, K_d, K_h, K_i, K_j, K_k, K_l, K_n, K_s, K_w, K_x

from utils.Constants import Constants
from utils.Utils import Utils


class Presets:
    # Player attributes
    PLAYER_DEFAULT_HEALTH = 100
    PLAYER_DEFAULT_SPEED = Axis(7, 5)
    PLAYER_BALANCE_WEAPON = Weapon(
        shoot_delay=125,
        weapon_type="triple",
        bullet=Bullet(speed=Axis(0, -20), sprite=Utils.scale_image(Constants.SPRITE_BULLET_BLUE, 0.2), damage=10)
    )

    PLAYER_PIERCE_WEAPON = Weapon(
        shoot_delay=300,
        weapon_type="single",
        bullet=Bullet(speed=Axis(0, -60), sprite=Utils.scale_image(Constants.SPRITE_BULLET_LIGHTBLUE, 0.2), damage=10, pierce=True)
    )

    PLAYER_FROG_WEAPON = Weapon(
        shoot_delay=200,
        weapon_type="spread",
        bullet=Bullet(speed=Axis(0, -20), sprite=Utils.scale_image(Constants.SPRITE_BULLET_GREEN, 0.2), damage=14)
    )

    PLAYER_SPEED_WEAPON = Weapon(
        shoot_delay=50,
        weapon_type="double",
        bullet=Bullet(speed=Axis(0, -25), sprite=Utils.scale_image(Constants.SPRITE_BULLET_RED, 0.2), damage=7)
    )

    ENEMY_WEAPON = Weapon(
        shoot_delay=350,
        weapon_type="random",
        bullet=Bullet(speed=Axis(0, 5), sprite=Utils.scale_image(Constants.SPRITE_ENEMY_BULLET, 0.2), tag=Constants.TAG_ENEMY)
    )

    PRIMARY_KB_LAYOUT = Layout(K_w, K_s, K_a, K_d, K_SPACE, K_x)
    SECONDARY_KB_LAYOUT = Layout(K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RSHIFT, K_RCTRL)
    EXTRA1_KB_LAYOUT = Layout(K_i, K_k, K_j, K_l, K_n, K_h)

    KEYBOARD_LAYOUTS = [PRIMARY_KB_LAYOUT, SECONDARY_KB_LAYOUT, EXTRA1_KB_LAYOUT, EXTRA1_KB_LAYOUT]

    CONTROLLER_LAYOUT = Layout(0.2, -0.2, 0.2, -0.2, 2, 10)
