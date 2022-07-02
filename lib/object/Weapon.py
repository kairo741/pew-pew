from object.Axis import Axis
from object.Bullet import Bullet

from pygame import Surface


class Weapon:
    def __init__(self, shoot_delay, bullet_sprite, weapon_type):
        self.shoot_delay = shoot_delay
        self.bullet_sprite = bullet_sprite
        self.weapon_type = weapon_type

    def create_bullet(self, x, y, speed=Axis(0, -20)):
        new_bullet = Bullet(x=x, y=y, speed=speed, sprite=Surface.copy(self.bullet_sprite))
        new_bullet.set_size_with_sprite()
        new_bullet.center()
        return new_bullet


    def make_bullets(self, spawn_position, speed=Axis(0, -20)):
        bullets = []

        if (self.weapon_type == "single"):
            bullets.append(self.create_bullet(spawn_position.x, spawn_position.y, speed))

        elif (self.weapon_type == "double"):
            bullets.append(self.create_bullet(x=spawn_position.x-10, y=spawn_position.y, speed=speed))
            bullets.append(self.create_bullet(x=spawn_position.x+10, y=spawn_position.y, speed=speed))

        elif (self.weapon_type == "triple"):
            bullets.append(self.create_bullet(x=spawn_position.x-20, y=spawn_position.y, speed=speed))
            bullets.append(self.create_bullet(x=spawn_position.x, y=spawn_position.y, speed=speed))
            bullets.append(self.create_bullet(x=spawn_position.x+20, y=spawn_position.y, speed=speed))
            
        return bullets
