from object.Axis import Axis
from object.Bullet import Bullet

from pygame import Surface


class Weapon:
    def __init__(self, shoot_delay, bullet_sprite, weapon_type):
        self.shoot_delay = shoot_delay
        self.bullet_sprite = bullet_sprite
        self.weapon_type = weapon_type

    def make_bullets(self, spawn_position):
        bullets = []

        if (self.weapon_type == "single"):
            new_bullet = Bullet(x=spawn_position.x, y=spawn_position.y, speed=Axis(
                0, -20), sprite=Surface.copy(self.bullet_sprite))
            new_bullet.setSizeWithSprite()
            new_bullet.center()
            
            bullets.append(new_bullet)

        elif (self.weapon_type == "double"):
            new_bullet = Bullet(x=spawn_position.x-10, y=spawn_position.y, speed=Axis(
                0, -20), sprite=Surface.copy(self.bullet_sprite))
            new_bullet.setSizeWithSprite()
            new_bullet.center()
            
            bullets.append(new_bullet)

            new_bullet = None
            new_bullet = Bullet(x=spawn_position.x+10, y=spawn_position.y, speed=Axis(
                0, -20), sprite=Surface.copy(self.bullet_sprite))
            new_bullet.setSizeWithSprite()
            new_bullet.center()
            
            bullets.append(new_bullet)

        elif (self.weapon_type == "triple"):
            new_bullet = Bullet(x=spawn_position.x-20, y=spawn_position.y, speed=Axis(
                0, -20), sprite=Surface.copy(self.bullet_sprite))
            new_bullet.setSizeWithSprite()
            new_bullet.center()
            
            bullets.append(new_bullet)

            new_bullet = None
            new_bullet = Bullet(x=spawn_position.x, y=spawn_position.y, speed=Axis(
                0, -20), sprite=Surface.copy(self.bullet_sprite))
            new_bullet.setSizeWithSprite()
            new_bullet.center()
            
            bullets.append(new_bullet)
            
            new_bullet = None
            new_bullet = Bullet(x=spawn_position.x+20, y=spawn_position.y, speed=Axis(
                0, -20), sprite=Surface.copy(self.bullet_sprite))
            new_bullet.setSizeWithSprite()
            new_bullet.center()
            
            bullets.append(new_bullet)
            
        return bullets
