import pygame

from code.modules import constants

vec = pygame.math.Vector2


class Star(pygame.sprite.Sprite):
    def __init__(self, top, left, color):
        super(Star, self).__init__()
        self.rect = pygame.rect.Rect(left, top, constants.star_width, constants.star_height)
        self.color = color

    def update(self):
        self.rect.x -= constants.star_speed
        if self.rect.right <= 0:
            self.kill()
