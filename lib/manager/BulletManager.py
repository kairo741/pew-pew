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
        if (bullet.y < -bullet.size.y):
            self.bullets.remove(bullet)

        elif (bullet.x < -bullet.size.x):
            self.bullets.remove(bullet)

        elif (bullet.x > screen_size.x):
            self.bullets.remove(bullet)

        elif (bullet.y > screen_size.y):
            self.bullets.remove(bullet)

            

    def has_collided(self, object, *actions):
        for bullet in self.bullets:
            if bullet.collided_with(object):
                try:
                    for action in actions:
                        action(bullet)
                except:
                    print("error in bullet collision action")

                if (bullet.pierce == False):
                    try:
                        self.bullets.remove(bullet)
                    except:
                        print("error removing bullet")
