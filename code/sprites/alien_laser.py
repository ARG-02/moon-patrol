import pygame

from code.modules import constants

vec = pygame.math.Vector2


class AlienLaser(pygame.sprite.Sprite):
    def __init__(self, initial_pos, variant=0):
        super(AlienLaser, self).__init__()
        self.rect = pygame.rect.Rect(initial_pos[0], initial_pos[1], constants.alien_laser_width, constants.alien_laser_height)
        self.rect.midtop = initial_pos
        self.variant = variant

    def update(self, ground):
        self.rect.y += constants.alien_laser_speed
        if self.is_colliding_with_ground(ground):
            if self.variant == 2:
                return True
            self.kill()

        if self.rect.bottom <= 0:
            self.kill()

    def is_colliding_with_ground(self, ground):
        gets_hit = pygame.Rect.colliderect(self.rect, ground)
        if gets_hit:
            return True
