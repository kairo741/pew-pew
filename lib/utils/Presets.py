from lib.object.Axis import Axis
from lib.object.Bullet import Bullet
from lib.object.BulletHeal import BulletHeal
from lib.object.BulletPierce import BulletPierce
from lib.object.Layout import Layout
from lib.object.Player import Player
from lib.object.PlayerVampire import PlayerVampire
from lib.object.Weapon import Weapon
from lib.utils.Constants import Constants
from lib.utils.Utils import Utils
from pygame import (K_DELETE, K_DOWN, K_END, K_HOME, K_INSERT, K_LEFT,
                    K_PAGEDOWN, K_PAGEUP, K_RCTRL, K_RIGHT, K_RSHIFT, K_SPACE,
                    K_UP, K_a, K_d, K_h, K_i, K_j, K_k, K_l, K_n, K_s, K_w,
                    K_x)


class Presets:
    # Player attributes
    PLAYER_DEFAULT_HEALTH = 100
    PLAYER_LIGHT_HEALTH = PLAYER_DEFAULT_HEALTH * 0.8
    PLAYER_HEAVY_HEALTH = PLAYER_DEFAULT_HEALTH * 1.2

    PLAYER_DEFAULT_SPEED = Axis(7, 5)
    PLAYER_LIGHT_SPEED = PLAYER_DEFAULT_SPEED.scale_to(1.2)
    PLAYER_HEAVY_SPEED = PLAYER_DEFAULT_SPEED.scale_to(0.8)

    PLAYER_BALANCE_WEAPON = Weapon(
        shoot_delay=170,
        weapon_type="triple",
        bullet=Bullet(speed=Axis(0, -20), sprite=Utils.scale_image(Constants.SPRITE_BULLET_BLUE, 0.2), damage=15)
    )

    PLAYER_PIERCE_WEAPON = Weapon(
        shoot_delay=300,
        weapon_type="single",
        bullet=BulletPierce(speed=Axis(0, -75), sprite=Utils.scale_image(Constants.SPRITE_BULLET_LIGHTBLUE_LONG, 0.2),
                            damage=75)
    )

    PLAYER_SPEED_WEAPON = Weapon(
        shoot_delay=70,
        weapon_type="double",
        bullet=Bullet(speed=Axis(0, -25), sprite=Utils.scale_image(Constants.SPRITE_BULLET_RED, 0.2), damage=10)
    )

    PLAYER_FROG_WEAPON = Weapon(
        shoot_delay=200,
        weapon_type="spread",
        bullet=Bullet(speed=Axis(0, -20), sprite=Utils.scale_image(Constants.SPRITE_BULLET_GREEN, 0.2), damage=18)
    )

    PLAYER_BAT_WEAPON = Weapon(
        shoot_delay=120,
        weapon_type="wiggle",
        bullet=BulletHeal(speed=Axis(0, -20), sprite=Utils.scale_image(Constants.SPRITE_BULLET_PURPLE, 0.2), damage=26)
    )

    ENEMY_DEFAULT_WEAPON = Weapon(
        shoot_delay=350,
        weapon_type="single",
        bullet=Bullet(speed=Axis(0, 5), sprite=Utils.scale_image(Constants.SPRITE_ENEMY_BULLET, 0.2),
                      tag=Constants.TAG_ENEMY)
    )

    ENEMY_EXPLOSION_WEAPON = Weapon(
        shoot_delay=900,
        weapon_type="explosion",
        bullet=Bullet(speed=Axis(0, 2), sprite=Utils.scale_image(Constants.SPRITE_ENEMY_BULLET, 0.2),
                      tag=Constants.TAG_ENEMY)
    )

    PLAYER_WEAPONS = [PLAYER_BALANCE_WEAPON, PLAYER_PIERCE_WEAPON, PLAYER_SPEED_WEAPON, PLAYER_FROG_WEAPON, PLAYER_BAT_WEAPON]
    PLAYER_SPEEDS = [PLAYER_DEFAULT_SPEED, PLAYER_DEFAULT_SPEED, PLAYER_LIGHT_SPEED, PLAYER_HEAVY_SPEED, PLAYER_DEFAULT_SPEED]
    PLAYER_HEALTHS = [PLAYER_DEFAULT_HEALTH, PLAYER_DEFAULT_HEALTH, PLAYER_LIGHT_HEALTH, PLAYER_HEAVY_HEALTH, PLAYER_LIGHT_HEALTH]
    
    PLAYER_BALANCE = Player(
        speed=PLAYER_SPEEDS[0],
        sprite=Constants.SPRITE_PLAYERS[0],
        health=PLAYER_HEALTHS[0],
        weapon=PLAYER_WEAPONS[0]
    )
    
    PLAYER_PIERCE = Player(
        speed=PLAYER_SPEEDS[1],
        sprite=Constants.SPRITE_PLAYERS[1],
        health=PLAYER_HEALTHS[1],
        weapon=PLAYER_WEAPONS[1]
    )
    
    PLAYER_SPEED = Player(
        speed=PLAYER_SPEEDS[2],
        sprite=Constants.SPRITE_PLAYERS[2],
        health=PLAYER_HEALTHS[2],
        weapon=PLAYER_WEAPONS[2]
    )
    
    PLAYER_FROGGERS = Player(
        speed=PLAYER_SPEEDS[3],
        sprite=Constants.SPRITE_PLAYERS[3],
        health=PLAYER_HEALTHS[3],
        weapon=PLAYER_WEAPONS[3]
    )

    PLAYER_VAMPIRE = PlayerVampire(
        speed=PLAYER_SPEEDS[4],
        sprite=Constants.SPRITE_PLAYERS[4],
        health=PLAYER_HEALTHS[4],
        weapon=PLAYER_WEAPONS[4]
    )

    PLAYER_LIST = [PLAYER_BALANCE, PLAYER_PIERCE, PLAYER_SPEED, PLAYER_FROGGERS]

    PRIMARY_KB_LAYOUT = Layout(K_w, K_s, K_a, K_d, K_SPACE, K_x)
    SECONDARY_KB_LAYOUT = Layout(K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RSHIFT, K_RCTRL)
    EXTRA1_KB_LAYOUT = Layout(K_i, K_k, K_j, K_l, K_n, K_h)
    EXTRA2_KB_LAYOUT = Layout(K_HOME, K_END, K_DELETE, K_PAGEDOWN, K_INSERT, K_PAGEUP)

    KEYBOARD_LAYOUTS = [PRIMARY_KB_LAYOUT, SECONDARY_KB_LAYOUT, EXTRA1_KB_LAYOUT, EXTRA2_KB_LAYOUT]

    CONTROLLER_LAYOUT = Layout(-0.2, 0.2, -0.2, 0.2, 2, 10)
