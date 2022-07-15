from os import path
from pygame import image, mixer, font, USEREVENT


class Constants:
    ROOT_PATH = path.abspath(path.join(path.dirname(__file__), "..\..", ""))

    # Colors
    BACKGROUND_COLOR = (14, 6, 21)
    COLOR_RED = (255, 50, 50)
    COLOR_GREY = (200, 200, 200)
    COLOR_BLUE = (100, 100, 255)
    COLOR_GREEN = (100, 255, 100)
    COLOR_GREEN_HEAL = (91, 247, 164)
    COLOR_LIGHT_BLUE = (0, 255, 255)

    # Game states
    RUNNING, PAUSE = 0, 1

    # Object Tags
    TAG_PLAYER = 0
    TAG_ENEMY = 1

    # Events
    ULTIMATE_END = USEREVENT + 1

    # ASSETS
    # Sprites
    SPRITE_STAR = image.load(ROOT_PATH + "\\assets\\images\\star.png")

    SPRITE_PLAYER_SHIP_BALANCE = image.load(ROOT_PATH + "\\assets\\images\\ship.png")
    SPRITE_BULLET_BLUE = image.load(ROOT_PATH + "\\assets\\images\\bullet_blue.png")

    SPRITE_PLAYER_SHIP_PIERCE = image.load(ROOT_PATH + "\\assets\\images\\ship_pierce.png")
    SPRITE_BULLET_LIGHTBLUE = image.load(ROOT_PATH + "\\assets\\images\\bullet_lightblue.png")
    SPRITE_BULLET_LIGHTBLUE_LONG = image.load(ROOT_PATH + "\\assets\\images\\bullet_lightblue_long.png")
    CRT_TV = image.load(ROOT_PATH + "\\assets\\images\\tv.png")

    SPRITE_PLAYER_SHIP_SPEED = image.load(ROOT_PATH + "\\assets\\images\\ship_speed.png")
    SPRITE_BULLET_RED = image.load(ROOT_PATH + "\\assets\\images\\bullet_red.png")

    SPRITE_PLAYER_SHIP_FROGGERS = image.load(ROOT_PATH + "\\assets\\images\\ship_froggers.png")
    SPRITE_BULLET_GREEN = image.load(ROOT_PATH + "\\assets\\images\\bullet_green.png")

    SPRITE_PLAYER_SHIP_32x32 = image.load(ROOT_PATH + "\\assets\\images\\ship_32x32.png")

    SPRITE_ENEMY_SHIP = image.load(ROOT_PATH + "\\assets\\images\\shipEnemy.png")
    SPRITE_ENEMY_BULLET = image.load(ROOT_PATH + "\\assets\\images\\enemy_bullet.png")

    POWER_UP_1 = image.load(ROOT_PATH + "\\assets\\images\\pwup-atk-up.png")
    POWER_UP_2 = image.load(ROOT_PATH + "\\assets\\images\\pwup-2.png")
    POWER_UP_3 = image.load(ROOT_PATH + "\\assets\\images\\pwup-atk-speed.png")
    POWER_UP_4 = image.load(ROOT_PATH + "\\assets\\images\\pwup-4.png")
    POWER_UP_5 = image.load(ROOT_PATH + "\\assets\\images\\pwup-5.png")
    POWER_UP_6 = image.load(ROOT_PATH + "\\assets\\images\\pwup-heal.png")
    POWER_UP_7 = image.load(ROOT_PATH + "\\assets\\images\\pwup-7.png")
    POWER_UP_8 = image.load(ROOT_PATH + "\\assets\\images\\pwup-8.png")

    SPRITE_PLAYERS = [SPRITE_PLAYER_SHIP_BALANCE, SPRITE_PLAYER_SHIP_PIERCE, SPRITE_PLAYER_SHIP_SPEED,
                      SPRITE_PLAYER_SHIP_FROGGERS]

    # Fonts
    FONT_NUMBER = ROOT_PATH + "\\assets\\fonts\\Montserrat-Regular.ttf"
    FONT_RETRO_GAMING = ROOT_PATH + "\\assets\\fonts\\Retro-Gaming.ttf"

    # Audio
    mixer.init()
    GLOBAL_VOLUME = 0
    SFX_VOLUME = GLOBAL_VOLUME * 1
    BGM_VOLUME = GLOBAL_VOLUME * 0.2

    # SFXs
    SFX_LASER = mixer.Sound(ROOT_PATH + "\\assets\\sfx\\laser.ogg")
    SFX_LASER_2 = mixer.Sound(ROOT_PATH + "\\assets\\sfx\\laser_2.ogg")
    SFX_EXPLOSION = mixer.Sound(ROOT_PATH + "\\assets\\sfx\\Explosion.mp3")
    SFX_DEATH = mixer.Sound(ROOT_PATH + "\\assets\\sfx\\death.ogg")
    SFX_TIME_STOP = mixer.Sound(ROOT_PATH + "\\assets\\sfx\\time_stop.mp3")

    SFX_LASER.set_volume(SFX_VOLUME * 0.3)
    SFX_LASER_2.set_volume(SFX_VOLUME * 0.3)
    SFX_EXPLOSION.set_volume(SFX_VOLUME * 0.2)
    SFX_DEATH.set_volume(SFX_VOLUME * 0.2)
    SFX_TIME_STOP.set_volume(SFX_VOLUME)

    # BGMs
    BGM_INDIGO = ROOT_PATH + "\\assets\\bgm\\indigo-946.mp3"
