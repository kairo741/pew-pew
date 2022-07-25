from lib.object.BulletBounce import BulletBounce
from lib.object.BulletHeal import BulletHeal
from lib.object.BulletPierce import BulletPierce


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

    def has_collided(self, bullet, object, *actions):
        self.check_collision(bullet, object, actions)

    def has_collided_any(self, object, *actions):
        for bullet in self.bullets:
            self.check_collision(bullet, object, actions)

    def check_collision(self, bullet, object, actions):
        if bullet.tag != object.tag:
            collision = bullet.collided_with(object, object.get_hitbox_rect())

            if collision:
                self.handle_bullet_collision(bullet, object, actions, collision)

        elif type(bullet) is BulletHeal:
            collision = bullet.collided_with(object)
            if collision and bullet.source_reference != object:
                self.try_remove_bullet(bullet)
                bullet.hit_callback(object, collision)

    def handle_bullet_collision(self, bullet, object, actions, collision):
        bullet.hit_callback(object, collision)
        self.try_execute_actions(bullet, actions)

        if type(bullet) is not BulletPierce and type(bullet) is not BulletBounce:
            self.try_remove_bullet(bullet)

        
    def try_execute_actions(self, bullet, actions):
        try:
            for action in actions:
                action(bullet)
        except:
            print("error in bullet collision action")

    def try_remove_bullet(self, bullet):
        try:
            self.bullets.remove(bullet)
        except:
            print("error removing bullet")
