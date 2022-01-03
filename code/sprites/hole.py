import pygame

from code.modules.constants import ground_speed
from code.modules import constants

vec = pygame.math.Vector2


class Hole(pygame.sprite.Sprite):
    def __init__(self, left, top, is_created=False):
        super(Hole, self).__init__()
        self.surf = pygame.image.load(f"content/textures/khud.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (constants.hole_width, self.surf.get_height() * constants.hole_width // self.surf.get_width()))
        self.rect = self.surf.get_rect()
        self.rect.left, self.rect.top = left, top - self.rect.height * constants.hole_whitespace
        self.has_crossed = False
        self.is_created = is_created

    def update(self):
        self.rect.x -= ground_speed
        if self.rect.right <= 0:
            self.kill()
