import pygame

from code.modules.constants import ground_speed

vec = pygame.math.Vector2


class Hole(pygame.sprite.Sprite):
    def __init__(self, left, top, width):
        super(Hole, self).__init__()
        self.surf = pygame.image.load(f"content/textures/khud.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (width, self.surf.get_height() * width // self.surf.get_width()))
        self.rect = self.surf.get_rect()
        self.rect.left, self.rect.top = left, top - self.rect.height//11
        self.has_crossed = False

    def update(self):
        self.rect.x -= ground_speed
        if self.rect.right <= 0:
            self.kill()
