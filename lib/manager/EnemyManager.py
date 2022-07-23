from random import randint, uniform

from pygame import time

from lib.object.Axis import Axis
from lib.object.Enemy import Enemy
from lib.utils.Constants import Constants
from lib.utils.Presets import Presets
from lib.utils.Utils import Utils


class EnemyManager:
    def __init__(self):
        super().__init__()
        self.enemies = []
        self.last_enemy = 0

    def reset(self):
        self.enemies = []
        self.last_enemy = 0

    def create_enemy(self, x, y, middle, player_quantity):
        if x < middle:
            speed_x = 2
        else:
            speed_x = -2

        if randint(1, 4) == 1:
            new_enemy = Enemy(
                x=x,
                y=y,
                sprite=Utils.scale_image(Constants.SPRITE_ENEMY_SHIP_BOMBER.convert_alpha(), 0.5),
                speed=Axis(uniform(0, speed_x), randint(1, 2)),
                weapon=Presets.ENEMY_EXPLOSION_WEAPON,
                health=90 + (player_quantity * 20)
            )
        else:
            new_enemy = Enemy(
                x=x,
                y=y,
                sprite=Utils.scale_image(Constants.SPRITE_ENEMY_SHIP.convert_alpha(), 0.5),
                speed=Axis(uniform(0, speed_x), randint(1, 2)),
                weapon=Presets.ENEMY_DEFAULT_WEAPON,
                health=90 + (player_quantity * 20)
            )

        new_enemy.set_size_with_sprite()
        new_enemy.center()
        new_enemy.y -= new_enemy.size.y
        return new_enemy

    def spawn_enemy_random(self, screen_size, player_quantity):
        if time.get_ticks() - self.last_enemy > randint(800 - (player_quantity * 50), 2000 - (player_quantity * 150)):
            self.enemies.append(
                self.create_enemy(
                    x=uniform(0, screen_size.x), y=0, middle=screen_size.x / 2,
                    player_quantity=player_quantity
                )
            )
            self.last_enemy = time.get_ticks()

    def manage_enemies(self, *actions):
        for enemy in self.enemies:
            for action in actions:
                action(enemy)

    def move_enemy(self, e, render_frame_time):
        e.x += e.speed.x * render_frame_time
        if e.y <= e.size.y:
            e.y += e.speed.y * 4 * render_frame_time
        else:
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

    def check_death(self, enemy, *actions):
        if enemy.health < 1:
            try:
                self.enemies.remove(enemy)
                for action in actions:
                    action(enemy)
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
