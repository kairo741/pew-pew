from object.BulletPierce import BulletPierce
from object.Bullet import Bullet
from object.Axis import Axis
from object.Layout import Layout
from object.Weapon import Weapon
from pygame import K_DELETE, K_DOWN, K_END, K_HOME, K_INSERT, K_LEFT, K_PAGEDOWN, K_PAGEUP, K_RCTRL, K_RIGHT, K_RSHIFT, \
    K_SPACE, K_UP, K_a, K_d, K_h, K_i, K_j, K_k, K_l, K_n, K_s, K_w, K_x

from utils.Constants import Constants
from utils.Utils import Utils


class Presets:
    # Player attributes
    PLAYER_DEFAULT_HEALTH = 100
    PLAYER_LIGHT_HEALTH = PLAYER_DEFAULT_HEALTH * 0.8
    PLAYER_HEAVY_HEALTH = PLAYER_DEFAULT_HEALTH * 1.2

    PLAYER_DEFAULT_SPEED = Axis(7, 5)
    PLAYER_LIGHT_SPEED = PLAYER_DEFAULT_SPEED.scale_to(1.2)
    PLAYER_HEAVY_SPEED = PLAYER_DEFAULT_SPEED.scale_to(0.8)

    PLAYER_BALANCE_WEAPON = Weapon(
        shoot_delay=125,
        weapon_type="triple",
        bullet=Bullet(speed=Axis(0, -20), sprite=Utils.scale_image(Constants.SPRITE_BULLET_BLUE, 0.2), damage=10)
    )

    PLAYER_PIERCE_WEAPON = Weapon(
        shoot_delay=300,
        weapon_type="single",
        bullet=BulletPierce(speed=Axis(0, -75), sprite=Utils.scale_image(Constants.SPRITE_BULLET_LIGHTBLUE_LONG, 0.2),
                            damage=70)
    )

    PLAYER_SPEED_WEAPON = Weapon(
        shoot_delay=65,
        weapon_type="double",
        bullet=Bullet(speed=Axis(0, -25), sprite=Utils.scale_image(Constants.SPRITE_BULLET_RED, 0.2), damage=9)
    )

    PLAYER_FROG_WEAPON = Weapon(
        shoot_delay=200,
        weapon_type="spread",
        bullet=Bullet(speed=Axis(0, -20), sprite=Utils.scale_image(Constants.SPRITE_BULLET_GREEN, 0.2), damage=18)
    )

    ENEMY_WEAPON = Weapon(
        shoot_delay=350,
        weapon_type="random",
        bullet=Bullet(speed=Axis(0, 5), sprite=Utils.scale_image(Constants.SPRITE_ENEMY_BULLET, 0.2),
                      tag=Constants.TAG_ENEMY)
    )

    PLAYER_WEAPONS = [PLAYER_BALANCE_WEAPON, PLAYER_PIERCE_WEAPON, PLAYER_SPEED_WEAPON, PLAYER_FROG_WEAPON]
    PLAYER_SPEEDS = [PLAYER_DEFAULT_SPEED, PLAYER_DEFAULT_SPEED, PLAYER_LIGHT_SPEED, PLAYER_HEAVY_SPEED]
    PLAYER_HEALTHS = [PLAYER_DEFAULT_HEALTH, PLAYER_DEFAULT_HEALTH, PLAYER_LIGHT_HEALTH, PLAYER_HEAVY_HEALTH]

    PRIMARY_KB_LAYOUT = Layout(K_w, K_s, K_a, K_d, K_SPACE, K_x)
    SECONDARY_KB_LAYOUT = Layout(K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RSHIFT, K_RCTRL)
    EXTRA1_KB_LAYOUT = Layout(K_i, K_k, K_j, K_l, K_n, K_h)
    EXTRA2_KB_LAYOUT = Layout(K_HOME, K_END, K_DELETE, K_PAGEDOWN, K_INSERT, K_PAGEUP)

    KEYBOARD_LAYOUTS = [PRIMARY_KB_LAYOUT, SECONDARY_KB_LAYOUT, EXTRA1_KB_LAYOUT, EXTRA2_KB_LAYOUT]

    CONTROLLER_LAYOUT = Layout(0.2, -0.2, 0.2, -0.2, 2, 10)
