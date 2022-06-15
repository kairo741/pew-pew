class BulletController:
    def __init__(self):
        super().__init__()
        self.bullets = []
        self.player_shot_bullet = 0
        self.player_fire_rate = 200

    def shoot(self, bullet):
        self.bullets.append(bullet)

    def move_bullets(self, render_time):
        for bullet in self.bullets:
            bullet.x += bullet.speed.x * render_time
            bullet.y += bullet.speed.y * render_time
            if (bullet.y < -30):
                self.bullets.remove(bullet)

    def render_bullets(self, screen):
        for bullet in self.bullets:
            bullet.render(screen)
            

    def has_collided(self, object, action):
        for bullet in self.bullets:
            if bullet.toRect().colliderect(object.toRect()):
                try:
                    action()
                except:
                    print("error in bullet collision action")

                try:
                    self.bullets.remove(bullet)
                except:
                    print("error removing bullet")
