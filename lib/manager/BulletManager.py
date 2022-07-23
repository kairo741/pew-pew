from lib.object.BulletHeal import BulletHeal
from lib.object.BulletPierce import BulletPierce
from lib.object.BulletBounce import BulletBounce
from lib.object.Axis import Axis
from random import uniform


class BulletManager:
    def __init__(self):
        super().__init__()
        self.bullets = []

    def reset(self):
        self.bullets = []

    def shoot(self, bullet):
        self.bullets.append(bullet)

    def manage_bullets(self, *actions):
        for bullet in self.bullets:
            for action in actions:
                action(bullet)

    def move_bullet(self, bullet, render_time):
        bullet.x += bullet.speed.x * render_time
        bullet.y += bullet.speed.y * render_time

    def check_bullet(self, bullet, screen_size):
        if bullet.y < -bullet.size.y:
            self.bullets.remove(bullet)

        elif bullet.x < -bullet.size.x:
            self.bullets.remove(bullet)

        elif bullet.x > screen_size.x:
            self.bullets.remove(bullet)

        elif bullet.y > screen_size.y:
            self.bullets.remove(bullet)

    def has_collided(self, bullet, object, *actions, use_hitbox=False):
        self.check_collision(bullet, object, actions, use_hitbox=use_hitbox)

    def has_collided_any(self, object, *actions, use_hitbox=False):
        for bullet in self.bullets:
            self.check_collision(bullet, object, actions, use_hitbox=use_hitbox)


    def check_collision(self, bullet, object, actions, use_hitbox=False):
        if bullet.tag != object.tag:
            if use_hitbox:
                collision = bullet.collided_with(object, object.get_hitbox_rect())
            else:
                collision = bullet.collided_with(object)

            if collision:
                self.handle_bullet_collision(bullet, object, actions, collision)
        
        elif type(bullet) is BulletHeal:
            if bullet.collided_with(object) and bullet.source_reference != object:
                self.try_remove_bullet(bullet)
                bullet.hit_callback(object)


    def handle_bullet_collision(self, bullet, object, actions, collision):
        if type(bullet) is BulletBounce:
            hits = [edge for edge in ['left', 'right'] if getattr(collision, edge) == getattr(bullet.to_rect(), edge)]
            bullet.speed = Axis(x=0, y=-bullet.speed.y)

            for hit in hits:
                horizontal_speed = uniform(abs(bullet.speed.y)*0.01, abs(bullet.speed.y*1.5))
                if hit == "left":
                    bullet.speed.x = horizontal_speed
                elif hit == "right":
                    bullet.speed.x = -horizontal_speed

        elif type(bullet) is not BulletPierce:
            self.try_remove_bullet(bullet)

        try:
            for action in actions:
                action(bullet)
        except:
            print("error in bullet collision action")

        bullet.hit_callback(object)
            
    
    def try_remove_bullet(self, bullet):
        try:
            self.bullets.remove(bullet)
        except:
            print("error removing bullet")