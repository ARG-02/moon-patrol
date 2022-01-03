import pygame

vec = pygame.math.Vector2


class AlienLaser(pygame.sprite.Sprite):
    def __init__(self, initial_pos, buggy_width, sc_width, type=0):
        super(AlienLaser, self).__init__()
        self.rect = pygame.rect.Rect(initial_pos[0], initial_pos[1], buggy_width // 12, buggy_width // 6)
        self.rect.midtop = initial_pos
        self.sc_width = sc_width
        self.type = type

    def update(self, ground):
        self.rect.y += self.rect.h // 2
        if self.is_colliding_with_ground(ground):
            if self.type == 2:
                return True
            self.kill()

        if self.rect.bottom <= 0:
            self.kill()

    def is_colliding_with_ground(self, ground):
        gets_hit = pygame.Rect.colliderect(self.rect, ground)
        if gets_hit:
            return True
