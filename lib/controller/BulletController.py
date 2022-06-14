class BulletController:
    def __init__(self):
        super().__init__()
        self.bullets = []
        self.player_shot_bullet = 0
        self.player_fire_rate = 200

    def shoot(self, bullet):
        self.bullets.append(bullet)

    def render_bullets(self, screen):
        for bullet in self.bullets:
            bullet.render(screen)
            bullet.x+=bullet.speed.x
            bullet.y += bullet.speed.y

    def has_collided(self, object, action):
        for bullet in self.bullets:
            if bullet.toRect().colliderect(object.toRect()):
                try:
                    action()
                except:
                    print("error in bullet colidor")
                
                try:
                    self.bullets.remove(bullet)
                except:
                    print("err remove enemy")
