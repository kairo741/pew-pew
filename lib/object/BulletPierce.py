from lib.utils.Constants import Constants
from .Bullet import Bullet

class BulletPierce(Bullet):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", damage=10, tag=Constants.TAG_PLAYER):
        super().__init__(x, y, size, speed, sprite, damage, tag)

        self.enemies_hit = []

    def collided_with(self, object, rect=None):
        collision_result = super().collided_with(object, rect)
        
        if collision_result:
            try:
                self.enemies_hit.index(object)
                return False

            except ValueError:
                self.enemies_hit.append(object)
                return True