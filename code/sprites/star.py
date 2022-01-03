import pygame

vec = pygame.math.Vector2


class Star(pygame.sprite.Sprite):
    def __init__(self, top, left, sc_width, color):
        super(Star, self).__init__()
        self.rect = pygame.rect.Rect(left, top, sc_width//120, sc_width//240)
        self.color = color

    def update(self):
        self.rect.x -= self.rect.w // 10
        if self.rect.right <= 0:
            self.kill()
