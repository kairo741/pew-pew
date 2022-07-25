from copy import deepcopy
from pygame import Surface
from lib.utils.Constants import Constants
from .Bullet import Bullet


class BulletPierce(Bullet):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", damage=10, tag=Constants.TAG_PLAYER,
                 source_reference=None):
        super().__init__(x, y, size, speed, sprite, damage, tag, source_reference)

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

    def copy(self):
        copy_obj = BulletPierce()
        for name, attr in self.__dict__.items():
            if type(attr) is Surface:
                copy_obj.__dict__[name] = Surface.copy(attr)
            else:
                copy_obj.__dict__[name] = deepcopy(attr)
        return copy_obj
