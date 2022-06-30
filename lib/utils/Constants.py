from os import path
from pygame import image, mixer, USEREVENT
from object.Weapon import Weapon
from utils.Utils import Utils

from object.Axis import Axis


class Constants:
    ROOT_PATH = path.abspath(path.join(path.dirname(__file__), '..\..', ''))
    
    # Colors
    BACKGROUND_COLOR = (14, 6, 21)

    # Game states
    RUNNING, PAUSE = 0, 1

    # Sprites
    SPRITE_STAR = image.load(ROOT_PATH + "\\assets\\images\\star.png")
    SPRITE_BULLET = image.load(ROOT_PATH + "\\assets\\images\\bullet.png")
    SPRITE_PLAYER_SHIP = image.load(ROOT_PATH + "\\assets\\images\\ship.png")
    SPRITE_PLAYER_SHIP_32x32 = image.load(ROOT_PATH + "\\assets\\images\\ship_32x32.png")
    SPRITE_ENEMY_SHIP = image.load(ROOT_PATH + "\\assets\\images\\shipEnemy.png")


    mixer.init()
    SFX_VOLUME = 1
    
    # SFXs
    SFX_EXPLOSION = mixer.Sound(ROOT_PATH + "\\assets\\sfx\\Explosion.mp3")
    SFX_TIME_STOP = mixer.Sound(ROOT_PATH + "\\assets\\sfx\\time_stop.mp3")
    SFX_LASER = mixer.Sound(ROOT_PATH + "\\assets\\sfx\\laser.ogg")
    SFX_DEATH = mixer.Sound(ROOT_PATH + "\\assets\\sfx\\death.ogg")
    
    SFX_EXPLOSION.set_volume(SFX_VOLUME*0.2)
    SFX_TIME_STOP.set_volume(SFX_VOLUME)
    SFX_LASER.set_volume(SFX_VOLUME*0.1)
    SFX_DEATH.set_volume(SFX_VOLUME*0.2)
    
    BGM_VOLUME = 0.1
    # BGMs
    BGM_INDIGO = ROOT_PATH + "\\assets\\bgm\\indigo-946.mp3"
    
    # Player attributes
    PLAYER_DEFAULT_HEALTH = 100
    PLAYER_DEFAULT_SPEED = Axis(10, 7)
    PLAYER_DEFAULT_WEAPON = Weapon(shoot_delay=100, weapon_type="triple",bullet_sprite=Utils.scale_image(SPRITE_BULLET, 0.2))

    ULTIMATE_END = USEREVENT+1




