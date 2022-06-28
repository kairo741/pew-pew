class BulletController:
    def __init__(self):
        super().__init__()
        self.bullets = []

    def shoot(self, bullet):
        self.bullets.append(bullet)

    def move_bullets(self, render_time, screen_size):
        for bullet in self.bullets:
            bullet.x += bullet.speed.x * render_time
            bullet.y += bullet.speed.y * render_time
            
            if (self.check_bullet(screen_size, bullet)):
                self.bullets.remove(bullet)
            
            
                
    def check_bullet(self, screen_size, bullet):
        if (bullet.y < -bullet.size.y):
            return True
            
        elif (bullet.x < -bullet.size.x):
            return True
            
        elif (bullet.x > screen_size.x):
            return True
        
        elif (bullet.y > screen_size.y):
            return True
    
        return False

    def render_bullets(self, screen):
        for bullet in self.bullets:
            bullet.render(screen)
            

    def has_collided(self, object, action):
        for bullet in self.bullets:
            if bullet.collided_with(object):
                try:
                    action(bullet)
                except:
                    print("error in bullet collision action")

                try:
                    self.bullets.remove(bullet)
                except:
                    print("error removing bullet")
