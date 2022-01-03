import pygame

vec = pygame.math.Vector2


class Mountain(pygame.sprite.Sprite):
    def __init__(self, left, sc_width, ground):
        super(Mountain, self).__init__()
        self.surf = pygame.image.load(f"content/textures/mountains.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (sc_width, self.surf.get_height() * sc_width // self.surf.get_width()))
        self.rect = self.surf.get_rect()
        self.rect.x, self.rect.y = left, ground.top - self.rect.height

    def update(self):
        self.rect.x -= self.rect.w // 200
        if self.rect.right <= self.rect.w // 200:
            self.kill()
