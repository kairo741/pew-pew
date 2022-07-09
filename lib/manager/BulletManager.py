from object.BulletPierce import BulletPierce

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

                if type(bullet) is not BulletPierce:
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

                    if type(bullet) is not BulletPierce:
                        try:
                            self.bullets.remove(bullet)
                        except:
                            print("error removing bullet")
