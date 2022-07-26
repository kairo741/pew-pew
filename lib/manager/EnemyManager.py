from random import randint, uniform

from pygame import time

from lib.object.Axis import Axis
from lib.object.EnemyBumper import EnemyBumper
from lib.object.PlayerSpeed import PlayerSpeed
from lib.utils.Presets import Presets


class EnemyManager:
    def __init__(self):
        super().__init__()
        self.enemies = []
        self.last_enemy = 0
        self.enemy_count = 0
        self.boss_spawned = False

    def reset(self):
        self.enemies = []
        self.last_enemy = 0
        self.enemy_count = 0
        self.boss_spawned = False

    def create_enemy(self, x, y, middle, player_quantity, is_boss=False, enemy_preset=None):
        if x < middle:
            speed_x = 2
        else:
            speed_x = -2

        enemy_speed = Axis(uniform(0, speed_x), randint(1, 2))
        if enemy_preset is None:
            if is_boss is False:
                if randint(1, 4) == 1:
                    new_enemy = Presets.ENEMY_BOMBER.copy()
                elif randint(1, 3) == 1:
                    new_enemy = Presets.ENEMY_RUNNER.copy()
                    enemy_speed.y = randint(8, 12)
                elif randint(1, 5) == 1:
                    new_enemy = Presets.ENEMY_BUMPER.copy()
                else:
                    new_enemy = Presets.ENEMY_DEFAULT.copy()
            else:
                new_enemy = Presets.BOSS_BUMPER.copy()
                enemy_speed = Axis(5, 0)
        else:
            new_enemy = enemy_preset.copy()

        if new_enemy.weapon != None:
            new_enemy.weapon.source_reference = new_enemy

        new_enemy.speed = enemy_speed
        new_enemy.health += (player_quantity * 20)
        new_enemy.max_health += (player_quantity * 20)

        new_enemy.set_size_with_sprite()
        new_enemy.center()
        new_enemy.x = x
        new_enemy.y = y - new_enemy.size.y
        return new_enemy

    def spawn_enemy_random(self, screen_size, player_quantity):
        if self.boss_spawned is False:
            if ((self.enemy_count + 1) % 31) == 0:
                self.enemies.append(self.create_enemy(x=screen_size.x / 2, y=200, middle=screen_size.x / 2,
                                                      player_quantity=player_quantity, is_boss=True))
                self.boss_spawned = True

            elif time.get_ticks() - self.last_enemy > randint(800 - (player_quantity * 50),
                                                              2000 - (player_quantity * 150)):
                self.append_enemy(screen_size, player_quantity)
        else:
            if time.get_ticks() - self.last_enemy > randint(6500 - (player_quantity * 50),
                                                            13000 - (player_quantity * 150)):
                boss = list(filter(lambda enemy: enemy.is_boss is True, self.enemies))
                if len(boss) > 0:
                    boss = boss[0]
                    self.append_enemy(screen_size, player_quantity, x=boss.x, y=boss.y, preset=Presets.ENEMY_BUMPER)

    def append_enemy(self, screen_size, player_quantity, x=None, y=None, preset=None):
        if x is not None and y is not None:
            enemy_x = x
            enemy_y = y
        else:
            enemy_x = uniform(0, screen_size.x)
            enemy_y = 0

        self.enemies.append(
            self.create_enemy(x=enemy_x, y=enemy_y, middle=screen_size.x / 2,
                              player_quantity=player_quantity, enemy_preset=preset))
        self.last_enemy = time.get_ticks()
        self.enemy_count += 1

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
        if type(enemy) is not EnemyBumper:
            if enemy.y < -(enemy.size.y * 2):
                self.enemies.remove(enemy)

            elif enemy.x < -(enemy.size.x * 2):
                self.enemies.remove(enemy)

            elif enemy.x > screen_size.x:
                self.enemies.remove(enemy)

            elif enemy.y > screen_size.y:
                self.enemies.remove(enemy)
        else:
            # TODO - refac
            enemy.enemy_passive(screen_size)

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

    def has_collided_player(self, enemy, player, *actions, render_frame_time=1):
        if type(player) == PlayerSpeed and player.ulted:
            if enemy.collided_with(player):
                enemy.take_damage((player.weapon.bullet.damage * 5) * render_frame_time)

        elif enemy.collided_with(player, player.get_hitbox_rect()):
            if not player.is_invincible:
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
