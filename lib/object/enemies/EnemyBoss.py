
from lib.object.enemies.Enemy import Enemy
from lib.utils.Constants import Constants


class EnemyBoss(Enemy):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, tag=Constants.TAG_ENEMY, level=1):
        super().__init__(x, y, size, speed, sprite, weapon, health, tag, level, on_screen=True)

    