class BulletController:
    def __init__(self, bullets):
        super().__init__(bullets)
        self.bullets = []

    def render_bullets(self):
        for bullet in self.bullets:
            bullet.render()

    def has_collided(self, object, action):
        for bullet in self.bullets:
            if bullet.toRect().colliderect(object.toRect()):
                action()
                try:
                    self.bullets.remove(bullet)
                except:
                    print("err remove enemy")
