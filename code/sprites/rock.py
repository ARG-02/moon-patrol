import pygame

from code.modules.constants import ground_speed
from code.modules import constants

vec = pygame.math.Vector2


class Rock(pygame.sprite.Sprite):
    def __init__(self, left, bottom):
        super(Rock, self).__init__()
        self.surf = pygame.image.load(f"content/textures/pud.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (constants.rock_width, self.surf.get_height() * constants.rock_width // self.surf.get_width()))
        self.rect = self.surf.get_rect()
        self.rect.left, self.rect.bottom = left, bottom
        self.has_crossed = False

        self.death_surfs = [pygame.image.load(f"content/animations/pud_death/{i}.png").convert_alpha() for i in range(3)]
        self.death_surfs = [pygame.transform.scale(i, (constants.rock_width, i.get_height() * constants.rock_width // i.get_width())) for i in self.death_surfs]

        self.death_frame = 0
        self.time_new_frame = 0
        self.is_dead = False

    def update(self):
        self.rect.x -= ground_speed
        if self.rect.right <= 0:
            self.kill()
        self.update_death_animation()

    def update_death_animation(self):
        if self.is_dead:
            if self.death_frame >= 3:
                self.kill()
                return None
            self.surf = self.death_surfs[self.death_frame]
            self.time_new_frame += 1
            if self.time_new_frame >= 4:
                self.time_new_frame = 0
                self.death_frame += 1
