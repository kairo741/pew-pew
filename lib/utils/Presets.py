
from utils.Constants import Constants
from object.Weapon import Weapon
from object.Axis import Axis
from utils.Utils import Utils

class Presets:    
    # Player attributes
    PLAYER_DEFAULT_HEALTH = 100
    PLAYER_DEFAULT_SPEED = Axis(10, 7)
    PLAYER_DEFAULT_WEAPON = Weapon(
        shoot_delay=100,
        weapon_type="triple",
        bullet_sprite=Utils.scale_image(Constants.SPRITE_BULLET, 0.2),
        tag=Constants.TAG_PLAYER
    )