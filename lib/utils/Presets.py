from lib.object.game.Axis import Axis
from lib.object.bullets.Bullet import Bullet
from lib.object.bullets.BulletBounce import BulletBounce
from lib.object.bullets.BulletHeal import BulletHeal
from lib.object.bullets.BulletPierce import BulletPierce
from lib.object.bullets.BulletVamp import BulletVamp
from lib.object.enemies.Enemy import Enemy
from lib.object.enemies.EnemyBoss import EnemyBoss
from lib.object.players.PlayerBalance import PlayerBalance
from lib.object.players.PlayerBerserk import PlayerBerserk
from lib.object.players.PlayerCharge import PlayerCharge
from lib.object.players.PlayerFroggers import PlayerFroggers
from lib.object.players.PlayerHealer import PlayerHealer
from lib.object.players.PlayerPierce import PlayerPierce
from lib.object.players.PlayerSpeed import PlayerSpeed
from lib.object.players.PlayerVampire import PlayerVampire
from lib.object.game.Weapon import Weapon
from lib.utils.Constants import Constants
from lib.utils.Utils import Utils


class Presets:
    # Player attributes
    PLAYER_DEFAULT_HEALTH = 75

    PLAYER_DEFAULT_SPEED = Axis(7, 5)

    PLAYER_BALANCE_WEAPON = Weapon(
        shoot_delay=240,
        weapon_type="triple",
        bullet=BulletBounce(speed=Axis(0, -15), sprite=Utils.scale_image(Constants.SPRITE_BULLET_RUBBER, 0.2),
                            damage=12)
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
        bullet=BulletVamp(speed=Axis(0, -20), sprite=Utils.scale_image(Constants.SPRITE_BULLET_PURPLE, 0.2), damage=28)
    )

    PLAYER_HEAL_WEAPON = Weapon(
        shoot_delay=250,
        weapon_type="arc",
        bullet=BulletHeal(speed=Axis(0, -20), sprite=Utils.scale_image(Constants.SPRITE_BULLET_YELLOW, 0.2), damage=22)
    )

    PLAYER_CHARGE_WEAPON = Weapon(
        shoot_delay=180,
        weapon_type="single",
        bullet=Bullet(speed=Axis(0, -40), sprite=Utils.scale_image(Constants.SPRITE_BULLET_RED, 0.4), damage=7)
    )

    PLAYER_BERSERK_WEAPON = Weapon(
        shoot_delay=500,
        weapon_type="triple",
        bullet=Bullet(speed=Axis(0, -15), sprite=Utils.scale_image(Constants.SPRITE_BULLET_RED, 0.3), damage=4)
    )

    ENEMY_DEFAULT_WEAPON = Weapon(
        shoot_delay=350,
        weapon_type="random",
        bullet=Bullet(speed=Axis(0, 5), sprite=Utils.scale_image(Constants.SPRITE_ENEMY_BULLET, 0.2),
                      tag=Constants.TAG_ENEMY, damage=20)
    )

    ENEMY_EXPLOSION_WEAPON = Weapon(
        shoot_delay=900,
        weapon_type="explosion",
        bullet=Bullet(speed=Axis(0, 2), sprite=Utils.scale_image(Constants.SPRITE_ENEMY_BULLET, 0.2),
                      tag=Constants.TAG_ENEMY, damage=20)
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

    ENEMY_BUMPER = Enemy(
        sprite=Utils.scale_image(Constants.SPRITE_ENEMY_SHIP_BUMPER.convert_alpha(), 0.4),
        weapon=ENEMY_DEFAULT_WEAPON,
        health=300,
        on_screen=True
    )

    BOSS_BUMPER = EnemyBoss(
        sprite=Utils.scale_image(Constants.SPRITE_ENEMY_SHIP_BUMPER.convert_alpha(), 0.8),
        weapon=Weapon(
            shoot_delay=80,
            weapon_type="random",
            bullet=Bullet(speed=Axis(0, 5), sprite=Utils.scale_image(Constants.SPRITE_ENEMY_BULLET, 0.2),
                          tag=Constants.TAG_ENEMY, damage=40)
        ),
        health=4000
    )

    PLAYER_WEAPONS = [PLAYER_BALANCE_WEAPON, PLAYER_PIERCE_WEAPON, PLAYER_SPEED_WEAPON, PLAYER_FROG_WEAPON,
                      PLAYER_BAT_WEAPON, PLAYER_HEAL_WEAPON, PLAYER_CHARGE_WEAPON, PLAYER_BERSERK_WEAPON]

    PLAYER_BALANCE = PlayerBalance(
        speed=PLAYER_DEFAULT_SPEED,
        sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_BALANCE, 0.84).convert_alpha(),
        health=PLAYER_DEFAULT_HEALTH,
        weapon=PLAYER_WEAPONS[0]
    )

    PLAYER_PIERCE = PlayerPierce(
        speed=PLAYER_DEFAULT_SPEED,
        sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_PIERCE, 0.84).convert_alpha(),
        sprite_ult=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_PIERCE_ULT, 0.84).convert_alpha(),
        health=PLAYER_DEFAULT_HEALTH*0.8,
        weapon=PLAYER_WEAPONS[1]
    )

    PLAYER_SPEED = PlayerSpeed(
        speed=PLAYER_DEFAULT_SPEED.scale_to(1.2),
        sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_SPEED, 0.84).convert_alpha(),
        health=PLAYER_DEFAULT_HEALTH * 0.8,
        weapon=PLAYER_WEAPONS[2]
    )

    PLAYER_FROGGERS = PlayerFroggers(
        speed=PLAYER_DEFAULT_SPEED.scale_to(0.8),
        sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_FROGGERS, 0.84).convert_alpha(),
        health=PLAYER_DEFAULT_HEALTH * 1.2,
        weapon=PLAYER_WEAPONS[3]
    )

    PLAYER_VAMPIRE = PlayerVampire(
        speed=PLAYER_DEFAULT_SPEED,
        sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_VAMPIRE, 0.84).convert_alpha(),
        sprite_ult=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_VAMPIRE_OPEN, 0.84).convert_alpha(),
        health=PLAYER_DEFAULT_HEALTH * 0.7,
        weapon=PLAYER_WEAPONS[4]
    )
    PLAYER_HEALER = PlayerHealer(
        speed=PLAYER_DEFAULT_SPEED,
        sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_MERCY, 0.84).convert_alpha(),
        sprite_ult=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_MERCY_GOLD, 0.84).convert_alpha(),
        health=PLAYER_DEFAULT_HEALTH * 0.7,
        weapon=PLAYER_WEAPONS[5]
    )

    PLAYER_CHARGE = PlayerCharge(
        speed=PLAYER_DEFAULT_SPEED.scale_to(0.75),
        sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_CHARGE_GREEN, 0.84).convert_alpha(),
        sprite_mid=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_CHARGE_ORANGE, 0.84).convert_alpha(),
        sprite_full=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_CHARGE_RED, 0.84).convert_alpha(),
        health=PLAYER_DEFAULT_HEALTH * 1.5,
        weapon=PLAYER_WEAPONS[6]
    )

    PLAYER_BERSERK = PlayerBerserk(
        speed=PLAYER_DEFAULT_SPEED.scale_to(0.8),
        sprite=Utils.scale_image(Constants.SPRITE_PLAYER_SHIP_BERSERK, 0.84).convert_alpha(),
        health=PLAYER_DEFAULT_HEALTH * 2,
        weapon=PLAYER_WEAPONS[7]
    )

    PLAYER_LIST = [PLAYER_BALANCE, PLAYER_PIERCE, PLAYER_SPEED, PLAYER_FROGGERS, PLAYER_VAMPIRE, PLAYER_HEALER, PLAYER_CHARGE, PLAYER_BERSERK]

    PLAYER_DETAILS_LIST = [
        {
            "name": "Bouncer",
            "passive": "Passive Description",
            "ultimate": "Ultimate Description",
        },
        {
            "name": "Pierce",
            "passive": "Passive Description",
            "ultimate": "Ultimate Description",
        },
        {
            "name": "Speed",
            "passive": "Passive Description",
            "ultimate": "Ultimate Description",
        },
        {
            "name": "Froggers",
            "passive": "Passive Description",
            "ultimate": "Ultimate Description",
        },
        {
            "name": "Vampire",
            "passive": "Passive Description",
            "ultimate": "Ultimate Description",
        },
        {
            "name": "Healer",
            "passive": "Passive Description",
            "ultimate": "Ultimate Description",
        },
        {
            "name": "Charge",
            "passive": "Passive Description",
            "ultimate": "Ultimate Description",
        },
        {
            "name": "Berserk",
            "passive": "Passive Description",
            "ultimate": "Ultimate Description",
        },
    ]
