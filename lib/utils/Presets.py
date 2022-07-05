
from object.Axis import Axis
from object.Layout import Layout
from object.Weapon import Weapon
from pygame import K_DOWN, K_LEFT, K_LSHIFT, K_RETURN, K_RIGHT, K_RSHIFT, K_SPACE, K_UP, K_a, K_d, K_s, K_w, K_x

from utils.Constants import Constants
from utils.Utils import Utils


class Presets:
    # Player attributes
    PLAYER_DEFAULT_HEALTH = 100
    PLAYER_DEFAULT_SPEED = Axis(7, 5)
    PLAYER_DEFAULT_WEAPON = Weapon(
        shoot_delay=100,
        weapon_type="triple",
        bullet_sprite=Utils.scale_image(Constants.SPRITE_BULLET, 0.2),
        tag=Constants.TAG_PLAYER
    )

    PRIMARY_KB_LAYOUT = Layout(K_w, K_s, K_a, K_d, K_SPACE, K_x)
    SECONDARY_KB_LAYOUT = Layout(K_UP, K_DOWN, K_LEFT, K_RIGHT, K_RSHIFT, K_RETURN)

    KEYBOARD_LAYOUTS = [PRIMARY_KB_LAYOUT, SECONDARY_KB_LAYOUT]

    CONTROLLER_LAYOUT = Layout(0.2, -0.2, 0.2, -0.2, 2, 10)
