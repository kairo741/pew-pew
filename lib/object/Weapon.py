from copy import deepcopy
from random import randint

from pygame import Surface

from lib.object.Axis import Axis
from lib.object.Bullet import Bullet


class Weapon:
    def __init__(self, shoot_delay=0, weapon_type="single", bullet=Bullet()):
        self.shoot_delay = shoot_delay
        self.weapon_type = weapon_type
        self.bullet = bullet

    def copy(self):
        copyobj = Weapon(0, "single", Bullet())
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = deepcopy(attr)
        return copyobj

    def calculate_dps(self):
        shot_damage = 0

        for bullet in self.make_bullets(Axis(0, 0)):
            shot_damage+=bullet.damage

        shot_damage *= 1000 / self.shoot_delay

        return round(shot_damage)

    def create_bullet(self, x, y, override_speed=None):
        speed = self.bullet.speed
        if override_speed:
            speed = override_speed

        
        new_bullet = type(self.bullet)(x=x, y=y, speed=speed, sprite=Surface.copy(self.bullet.sprite.convert_alpha()), 
            tag=self.bullet.tag, 
            damage=self.bullet.damage
        )
        new_bullet.set_size_with_sprite()
        new_bullet.center()
        return new_bullet


    def make_bullets(self, spawn_position):
        bullets = []

        if self.weapon_type == "random":
            bullets.append(self.create_bullet(spawn_position.x, spawn_position.y, override_speed=Axis(randint(-2, 2), randint(4, 6))))

        if self.weapon_type == "single":
            bullets.append(self.create_bullet(spawn_position.x, spawn_position.y))

        elif self.weapon_type == "double":
            bullets.append(self.create_bullet(x=spawn_position.x-10, y=spawn_position.y))
            bullets.append(self.create_bullet(x=spawn_position.x+10, y=spawn_position.y))

        elif self.weapon_type == "triple":
            bullets.append(self.create_bullet(x=spawn_position.x-20, y=spawn_position.y))
            bullets.append(self.create_bullet(x=spawn_position.x, y=spawn_position.y))
            bullets.append(self.create_bullet(x=spawn_position.x+20, y=spawn_position.y))

        elif self.weapon_type == "spread":
            bullets.append(self.create_bullet(x=spawn_position.x-20, y=spawn_position.y, override_speed=Axis(-5, self.bullet.speed.y)))
            bullets.append(self.create_bullet(x=spawn_position.x, y=spawn_position.y))
            bullets.append(self.create_bullet(x=spawn_position.x+20, y=spawn_position.y, override_speed=Axis(5, self.bullet.speed.y)))
            
        return bullets
