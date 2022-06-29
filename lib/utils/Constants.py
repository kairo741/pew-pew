from os import path
from pygame import image, mixer
from object.Weapon import Weapon
from utils.Utils import Utils

from object.Axis import Axis


class Constants:
    ROOT_PATH = path.abspath(path.join(path.dirname(__file__), '..\..', ''))

    # Sprites
    SPRITE_STAR = image.load(ROOT_PATH + "\\assets\\images\\star.png")
    SPRITE_BULLET = image.load(ROOT_PATH + "\\assets\\images\\bullet.png")
    SPRITE_PLAYER_SHIP = image.load(ROOT_PATH + "\\assets\\images\\ship.png")
    SPRITE_PLAYER_SHIP_32x32 = image.load(ROOT_PATH + "\\assets\\images\\ship_32x32.png")
    SPRITE_ENEMY_SHIP = image.load(ROOT_PATH + "\\assets\\images\\shipEnemy.png")

    # SFXs
    # SFX_EXPLOSION = mixer.Sound(ROOT_PATH + "\\assets\\sfx\\Explosion.mp3")

    # Game states
    RUNNING, PAUSE = 0, 1

    # Player attributes
    PLAYER_DEFAULT_HEALTH = 100
    PLAYER_DEFAULT_SPEED = Axis(10, 7)
    PLAYER_DEFAULT_WEAPON = Weapon(shoot_delay=100, weapon_type="triple",
                                   bullet_sprite=Utils.scale_image(SPRITE_BULLET, 0.2))
