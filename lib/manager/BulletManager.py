from lib.object.BulletPierce import BulletPierce
from lib.object.BulletBounce import BulletBounce
from lib.object.Axis import Axis
from random import randint


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
        if bullet.tag != object.tag:
            if use_hitbox:
                collided = bullet.collided_with(object, object.get_hitbox_rect())
            else:
                collided = bullet.collided_with(object)

            if collided:
                try:
                    for action in actions:
                        action(bullet)
                except:
                    print("error in bullet collision action")

                bullet.hit_callback(object)
                if type(bullet) is BulletBounce:
                    try:
                        new_bullet = type(bullet)(x=bullet.x, y=bullet.y + 30, size=bullet.size,
                                                  speed=Axis(x=randint(-10, 10), y=bullet.speed.y * -0.3),
                                                  sprite=bullet.sprite)
                        self.bullets.remove(bullet)
                        self.bullets.append(new_bullet)
                    except:
                        print("error removing bullet")

                elif type(bullet) is not BulletPierce:
                    try:
                        self.bullets.remove(bullet)
                    except:
                        print("error removing bullet")

    def has_collided_any(self, object, *actions, use_hitbox=False):
        for bullet in self.bullets:
            if bullet.tag != object.tag:
                if use_hitbox:
                    collided = bullet.collided_with(object, object.get_hitbox_rect())
                else:
                    collided = bullet.collided_with(object)

                if collided:
                    try:
                        for action in actions:
                            action(bullet)
                    except:
                        print("error in bullet collision action")

                    bullet.hit_callback(object)
                    if type(bullet) is BulletBounce:
                        try:
                            new_bullet = type(bullet)(x=bullet.x, y=bullet.y + 30, size=bullet.size,
                                                      speed=Axis(x=randint(-10, 10), y=bullet.speed.y * -0.3),
                                                      sprite=bullet.sprite)
                            self.bullets.remove(bullet)
                            self.bullets.append(new_bullet)
                        except:
                            print("error removing bullet")

                    elif type(bullet) is not BulletPierce:
                        try:
                            self.bullets.remove(bullet)
                        except:
                            print("error removing bullet")
