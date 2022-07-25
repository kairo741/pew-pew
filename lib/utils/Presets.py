from lib.object.Axis import Axis
from lib.object.Bullet import Bullet
from lib.object.BulletBounce import BulletBounce
from lib.object.BulletHeal import BulletHeal
from lib.object.BulletPierce import BulletPierce
from lib.object.BulletVamp import BulletVamp
from lib.object.Enemy import Enemy
from lib.object.EnemyBumper import EnemyBumper
from lib.object.Player import Player
from lib.object.PlayerHealer import PlayerHealer
from lib.object.PlayerVampire import PlayerVampire
from lib.object.Weapon import Weapon
from lib.utils.Constants import Constants
from lib.utils.Utils import Utils


class Presets:
    # Player attributes
    PLAYER_DEFAULT_HEALTH = 100

    PLAYER_DEFAULT_SPEED = Axis(7, 5)

    PLAYER_BALANCE_WEAPON = Weapon(
        shoot_delay=200,
        weapon_type="triple",
        bullet=BulletBounce(speed=Axis(0, -15), sprite=Utils.scale_image(Constants.SPRITE_BULLET_RUBBER, 0.2), damage=12)
    )

    PLAYER_PIERCE_WEAPON = Weapon(
        shoot_delay=300,
        weapon_type="single",
        bullet=BulletPierce(speed=Axis(0, -60), sprite=Utils.scale_image(Constants.SPRITE_BULLET_LIGHTBLUE_LONG, 0.2),
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
        bullet=BulletVamp(speed=Axis(0, -20), sprite=Utils.scale_image(Constants.SPRITE_BULLET_PURPLE, 0.2), damage=26)
    )

    PLAYER_HEAL_WEAPON = Weapon(
        shoot_delay=250,
        weapon_type="sides",
        bullet=BulletHeal(speed=Axis(0, -20), sprite=Utils.scale_image(Constants.SPRITE_BULLET_YELLOW, 0.2), damage=22)
    )

    ENEMY_DEFAULT_WEAPON = Weapon(
        shoot_delay=350,
        weapon_type="random",
        bullet=Bullet(speed=Axis(0, 5), sprite=Utils.scale_image(Constants.SPRITE_ENEMY_BULLET, 0.2),
                      tag=Constants.TAG_ENEMY)
    )

    ENEMY_EXPLOSION_WEAPON = Weapon(
        shoot_delay=900,
        weapon_type="explosion",
        bullet=Bullet(speed=Axis(0, 2), sprite=Utils.scale_image(Constants.SPRITE_ENEMY_BULLET, 0.2),
                      tag=Constants.TAG_ENEMY)
    )

    ENEMY_DEFAULT = Enemy(
        sprite=Utils.scale_image(Constants.SPRITE_ENEMY_SHIP.convert_alpha(), 0.5),
        weapon=ENEMY_DEFAULT_WEAPON,
        health=80
    )

    ENEMY_BOMBER = Enemy(
        sprite=Utils.scale_image(Constants.SPRITE_ENEMY_SHIP_BOMBER.convert_alpha(), 0.5),
        weapon=ENEMY_EXPLOSION_WEAPON,
        health=110
    )

    ENEMY_RUNNER = Enemy(
        sprite=Utils.scale_image(Constants.SPRITE_ENEMY_SHIP_RUNNER.convert_alpha(), 0.4),
        weapon=None,
        health=50
    )

    ENEMY_BUMPER = EnemyBumper(
        sprite=Utils.scale_image(Constants.SPRITE_ENEMY_SHIP_BUMPER.convert_alpha(), 0.4),
        weapon=ENEMY_DEFAULT_WEAPON,
        health=300
    )

    PLAYER_WEAPONS = [PLAYER_BALANCE_WEAPON, PLAYER_PIERCE_WEAPON, PLAYER_SPEED_WEAPON, PLAYER_FROG_WEAPON, PLAYER_BAT_WEAPON, PLAYER_HEAL_WEAPON]

    PLAYER_BALANCE = Player(
        speed=PLAYER_DEFAULT_SPEED,
        sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_BALANCE, 0.84).convert_alpha(),
        health=PLAYER_DEFAULT_HEALTH,
        weapon=PLAYER_WEAPONS[0]
    )

    PLAYER_PIERCE = Player(
        speed=PLAYER_DEFAULT_SPEED,
        sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_PIERCE, 0.84).convert_alpha(),
        health=PLAYER_DEFAULT_HEALTH,
        weapon=PLAYER_WEAPONS[1]
    )

    PLAYER_SPEED = Player(
        speed=PLAYER_DEFAULT_SPEED.scale_to(1.2),
        sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_SPEED, 0.84).convert_alpha(),
        health=PLAYER_DEFAULT_HEALTH*0.8,
        weapon=PLAYER_WEAPONS[2]
    )

    PLAYER_FROGGERS = Player(
        speed=PLAYER_DEFAULT_SPEED.scale_to(0.8),
        sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_FROGGERS, 0.84).convert_alpha(),
        health=PLAYER_DEFAULT_HEALTH*1.2,
        weapon=PLAYER_WEAPONS[3]
    )

    PLAYER_VAMPIRE = PlayerVampire(
        speed=PLAYER_DEFAULT_SPEED,
        sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_VAMPIRE, 0.84).convert_alpha(),
        health=PLAYER_DEFAULT_HEALTH*0.7,
        weapon=PLAYER_WEAPONS[4]
    )
    PLAYER_HEALER = PlayerHealer(
        speed=PLAYER_DEFAULT_SPEED,
        sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_MERCY, 0.84).convert_alpha(),
        health=PLAYER_DEFAULT_HEALTH*0.7,
        weapon=PLAYER_WEAPONS[5]
    )

    PLAYER_LIST = [PLAYER_BALANCE, PLAYER_PIERCE, PLAYER_SPEED, PLAYER_HEALER, PLAYER_VAMPIRE, PLAYER_FROGGERS]
