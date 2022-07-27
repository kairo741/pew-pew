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
    COLOR_YELLOW = (250, 255, 97)

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
    SPRITE_GLOW = image.load(ROOT_PATH + "\\assets\\images\\glow.png")
    CRT_TV = image.load(ROOT_PATH + "\\assets\\images\\tv.png")

    SPRITE_PLAYER_SHIP_BALANCE = image.load(ROOT_PATH + "\\assets\\images\\ships\\ship.png")
    SPRITE_PLAYER_SHIP_PIERCE = image.load(ROOT_PATH + "\\assets\\images\\ships\\ship_pierce.png")
    SPRITE_PLAYER_SHIP_SPEED = image.load(ROOT_PATH + "\\assets\\images\\ships\\ship_speed.png")
    SPRITE_PLAYER_SHIP_FROGGERS = image.load(ROOT_PATH + "\\assets\\images\\ships\\ship_froggers.png")
    SPRITE_PLAYER_SHIP_VAMPIRE = image.load(ROOT_PATH + "\\assets\\images\\ships\\ship_vampire.png")
    SPRITE_PLAYER_SHIP_MERCY = image.load(ROOT_PATH + "\\assets\\images\\ships\\ship_mercy.png")
    SPRITE_PLAYER_SHIP_CHARGE_ORANGE = image.load(ROOT_PATH + "\\assets\\images\\ships\\ship_charge_orange.png")
    SPRITE_PLAYER_SHIP_CHARGE_GREEN = image.load(ROOT_PATH + "\\assets\\images\\ships\\ship_charge_green.png")
    SPRITE_PLAYER_SHIP_CHARGE_RED = image.load(ROOT_PATH + "\\assets\\images\\ships\\ship_charge_red.png")

    SPRITE_BULLET_BLUE = image.load(ROOT_PATH + "\\assets\\images\\bullets\\bullet_blue.png")
    SPRITE_BULLET_LIGHTBLUE = image.load(ROOT_PATH + "\\assets\\images\\bullets\\bullet_lightblue.png")
    SPRITE_BULLET_LIGHTBLUE_LONG = image.load(ROOT_PATH + "\\assets\\images\\bullets\\bullet_lightblue_long.png")
    SPRITE_BULLET_RED = image.load(ROOT_PATH + "\\assets\\images\\bullets\\bullet_red.png")
    SPRITE_BULLET_GREEN = image.load(ROOT_PATH + "\\assets\\images\\bullets\\bullet_green.png")
    SPRITE_BULLET_PURPLE = image.load(ROOT_PATH + "\\assets\\images\\bullets\\bullet_purple.png")
    SPRITE_BULLET_YELLOW = image.load(ROOT_PATH + "\\assets\\images\\bullets\\bullet_yellow.png")
    SPRITE_BULLET_RUBBER = image.load(ROOT_PATH + "\\assets\\images\\bullets\\bullet_rubber.png")
    SPRITE_BULLET_FROGGERS_ULT = image.load(ROOT_PATH + "\\assets\\images\\bullets\\froggers_ult_bullet.png")

    SPRITE_PLAYER_SHIP_32x32 = image.load(ROOT_PATH + "\\assets\\images\\ship_32x32.png")

    SPRITE_ENEMY_SHIP = image.load(ROOT_PATH + "\\assets\\images\\enemies\\ship_enemy.png")
    SPRITE_ENEMY_SHIP_BOMBER = image.load(ROOT_PATH + "\\assets\\images\\enemies\\ship_enemy_bomber.png")
    SPRITE_ENEMY_SHIP_RUNNER = image.load(ROOT_PATH + "\\assets\\images\\enemies\\ship_enemy_runner.png")
    SPRITE_ENEMY_SHIP_BUMPER = image.load(ROOT_PATH + "\\assets\\images\\enemies\\ship_enemy_bumper.png")

    SPRITE_ENEMY_BULLET = image.load(ROOT_PATH + "\\assets\\images\\bullets\\enemy_bullet.png")

    SPRITE_POWER_UP_ATK = image.load(ROOT_PATH + "\\assets\\images\\power_ups\\atk_disk.png")
    SPRITE_POWER_UP_SPEED = image.load(ROOT_PATH + "\\assets\\images\\power_ups\\speed_disk.png")
    SPRITE_POWER_UP_HEAL = image.load(ROOT_PATH + "\\assets\\images\\power_ups\\heal_disk.png")
    SPRITE_POWER_UP_RANDOM = image.load(ROOT_PATH + "\\assets\\images\\power_ups\\random_disk.png")
    SPRITE_POWER_UP_CHARGE_ULT = image.load(ROOT_PATH + "\\assets\\images\\power_ups\\ult_disk.png")

    font.init()
    # Fonts
    FONT_NUMBER = ROOT_PATH + "\\assets\\fonts\\Montserrat-Regular.ttf"
    FONT_RETRO_GAMING = ROOT_PATH + "\\assets\\fonts\\Retro-Gaming.ttf"

    FONT_LEVEL_OBJECT = font.Font(FONT_RETRO_GAMING, 16)

    # Audio
    mixer.init()
    GLOBAL_VOLUME = 1
    SFX_MIXER_CHANNEL = 1
    BGM_MIXER_CHANNEL = 2
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
