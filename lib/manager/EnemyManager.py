from pygame import time, Surface
from random import randint, uniform

from object.Weapon import Weapon
from object.Axis import Axis
from object.Enemy import Enemy
from utils.Constants import Constants
from utils.Utils import Utils


class EnemyManager:
    def __init__(self):
        super().__init__()
        self.enemy_sprite = Utils.scale_image(Constants.SPRITE_ENEMY_SHIP, 0.5)
        self.enemies = []
        self.last_enemy = 0

    def reset(self):
        self.enemies = []
        self.last_enemy = 0

    def create_enemy(self, x, y):
        new_enemy = Enemy(
            x=x,
            y=y,
            sprite=Surface.copy(self.enemy_sprite),
            speed=Axis(uniform(-2, 2), randint(1, 3)),
            weapon=Weapon(
                shoot_delay=500,
                weapon_type="single",
                bullet_sprite=Utils.scale_image(Constants.SPRITE_ENEMY_BULLET, 0.2),
            ),
        )
        new_enemy.set_size_with_sprite()
        new_enemy.center()
        return new_enemy

    def spawn_enemy_random(self, screen_size):
        if time.get_ticks() - self.last_enemy > 800:
            sprite_size = self.enemy_sprite.get_size()
            self.enemies.append(
                self.create_enemy(
                    x=uniform(screen_size.x / 4, screen_size.x / 1.8), y=-sprite_size[1]
                )
            )
            self.last_enemy = time.get_ticks()

    def manage_enemies(self, *actions):
        for enemy in self.enemies:
            for action in actions:
                action(enemy)

    def move_enemy(self, e, render_frame_time):
        e.x += e.speed.x * render_frame_time
        e.y += e.speed.y * render_frame_time

    def check_enemy(self, enemy, screen_size):
        if enemy.y < -(enemy.size.y * 2):
            self.enemies.remove(enemy)

        elif enemy.x < -(enemy.size.x * 2):
            self.enemies.remove(enemy)

        elif enemy.x > screen_size.x:
            self.enemies.remove(enemy)

        elif enemy.y > screen_size.y:
            self.enemies.remove(enemy)

        elif enemy.health < 1:
            try:
                self.enemies.remove(enemy)
            except:
                print("error removing enemy")

    def has_collided_any(self, object, *actions):
        for enemy in self.enemies:
            if enemy.collided_with(object, object.get_hitbox_rect()):
                try:
                    for action in actions:
                        action(enemy)
                except:
                    print("error in enemy collision action")

    def has_collided(self, enemy, object, *actions):
        if enemy.collided_with(object, object.get_hitbox_rect()):
            try:
                for action in actions:
                    action(enemy)
            except:
                print("error in enemy collision action")
