import pygame

from code.modules import constants

vec = pygame.math.Vector2


class Mountain(pygame.sprite.Sprite):
    def __init__(self, left, ground):
        super(Mountain, self).__init__()
        self.surf = pygame.image.load(f"content/textures/mountains.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (constants.width, self.surf.get_height() * constants.width // self.surf.get_width()))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = left, ground.top - self.rect.height

    def update(self):
        self.rect.x -= constants.mountain_speed
        if self.rect.right <= constants.mountain_speed:
            self.kill()
            return True
