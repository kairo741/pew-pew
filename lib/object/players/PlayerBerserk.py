from lib.object.game.Ultimate import Ultimate
from lib.object.players.Player import Player
from pygame import time, draw, mask, Surface, SRCALPHA

class PlayerBerserk(Player):
    def __init__(self, x=0, y=0, size=..., speed=..., sprite="", weapon="", health=100, layout="", ultimate=Ultimate(), level=1):

        ultimate = Ultimate(enable_function=self.enable_ultimate, disable_function=self.disable_ultimate, duration=1, color=[0, 0, 0])
        super().__init__(x, y, size, speed, sprite, weapon, health, layout, ultimate, level)

        self.outline = Surface((0, 0))

        # 15 segundos de cooldown
        self.skill_cooldown = 15 * 1000
        self.last_skill = 0

        self.death_resistance_skill = True

    def set_size_with_sprite(self, set_glow=True):
        super().set_size_with_sprite(set_glow)

        self.set_outline()

    def set_outline(self):
        sprite_mask = mask.from_surface(self.sprite)
        mask_outline = sprite_mask.outline()
        self.outline = Surface(self.size.scale_to(2).to_list(), SRCALPHA).convert_alpha()
        outline_size = self.outline.get_size()
        
        for index, point in enumerate(mask_outline):
            mask_outline[index] = [point[0]+outline_size[0]/4, point[1]+outline_size[1]/4]
        
        draw.polygon(self.outline, (255, 50, 50), mask_outline, 3)

    def set_level(self, level):
        old_health = self.health
        super().set_level(level)
        
        self.health = old_health

    def player_passive(self, render_frame_time):
        if self.health > 1:
            self.health -= (self.health * 0.0003)*render_frame_time

        if not self.death_resistance_skill:
            if time.get_ticks() > self.last_skill+self.skill_cooldown:
                self.death_resistance_skill = True

        return super().player_passive(render_frame_time)

    def take_damage(self, value):
        if self.health - value <= 0 and self.death_resistance_skill:
            self.health = 1
            self.death_resistance_skill = False
            self.last_skill = time.get_ticks()

        else:        
            super().take_damage(value)

    def shoot(self, bullet_manager, damage_multiplier=1):
        damage_multiplier = (1+1-(self.health / self.max_health))**4
        shoot_delay_multiplier = self.health / self.max_health
        if shoot_delay_multiplier < 0.3:
            shoot_delay_multiplier = 0.3

        return super().shoot(bullet_manager, damage_multiplier, shoot_delay_multiplier)

    def enable_ultimate(self):
        super().enable_ultimate()
        self.health = 1
        self.death_resistance_skill = True


    def render(self, screen, render_frame_time, hide_hud=False):
        if self.death_resistance_skill:
            outline_size = self.outline.get_size()
            screen.blit(self.outline, (self.x-outline_size[0]/4, self.y-outline_size[1]/4))

        return super().render(screen, render_frame_time, hide_hud=hide_hud)
