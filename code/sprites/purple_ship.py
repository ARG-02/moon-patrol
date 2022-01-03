import pygame
import random

vec = pygame.math.Vector2


class PurpleShip(pygame.sprite.Sprite):
    def __init__(self, ground, ship_width, initial_pos, sc_dim, num_moves, mountain_top):
        super(PurpleShip, self).__init__()
        self.surfs = [pygame.image.load(f"content/animations/purple_ship/{i}.png").convert_alpha() for i in range(2)]
        self.surfs = [pygame.transform.scale(i, (ship_width, self.surfs[0].get_height() * ship_width // self.surfs[0].get_width())) for i in self.surfs]
        self.surf = self.surfs[0]
        self.rect = self.surfs[0].get_rect()
        self.frame = 0
        self.rect.left, self.rect.top = initial_pos
        self.sc_width, self.sc_height = sc_dim
        self.ground = ground
        self.lower_bound = mountain_top
        self.num_moves = num_moves  # 9-12
        self.direction_length = random.randint(90, 100)
        if initial_pos[0] > 0:
            self.horizontal_velocity = -1
        else:
            self.horizontal_velocity = 1
        self.vertical_velocity = 0
        self.movement_speed = ship_width // 20

        self.death_surfs = [pygame.image.load(f"content/animations/ship_death/{i}.png").convert_alpha() for i in
                            range(5)]
        self.death_surfs = [pygame.transform.scale(i, (ship_width, i.get_height() * ship_width // i.get_width())) for i in
                            self.death_surfs]

        self.death_frame = 0
        self.time_new_frame = 0
        self.is_dead = False

    def update_death_animation(self):
        if self.is_dead:
            self.surf = self.death_surfs[self.death_frame]
            self.time_new_frame += 1
            if self.time_new_frame >= 6:
                self.time_new_frame = 0
                self.death_frame += 1
            if self.death_frame >= 5:
                self.kill()

    def update_animation(self):
        self.frame += 1 if self.frame < 1 else -1
        self.surf = self.surfs[self.frame]

    def update(self):
        self.update_death_animation()
        if not self.is_dead:
            if self.num_moves > 1:
                if self.direction_length > 0:
                    self.direction_length -= 1
                else:
                    self.direction_length = random.randint(30, 50)
                    self.num_moves -= 1

                    if self.horizontal_velocity == 1:
                        self.vertical_velocity = 1
                        self.horizontal_velocity = 0
                    elif self.horizontal_velocity == -1:
                        self.vertical_velocity = -1
                        self.horizontal_velocity = 0
                    elif self.vertical_velocity == 1:
                        self.horizontal_velocity = -1
                        self.vertical_velocity = 0
                    else:
                        self.horizontal_velocity = 1
                        self.vertical_velocity = 0

                    if self.horizontal_velocity == 1 and self.rect.right + self.horizontal_velocity * self.movement_speed * self.direction_length > self.sc_width:
                        self.direction_length = int((self.sc_width - self.rect.right) / self.movement_speed)
                    elif self.horizontal_velocity == -1 and self.rect.left + self.horizontal_velocity * self.movement_speed * self.direction_length < 0:
                        self.direction_length = int(self.rect.left / self.movement_speed)
                    elif self.vertical_velocity == 1 and self.rect.bottom + self.vertical_velocity * self.movement_speed * self.direction_length > self.lower_bound:
                        self.direction_length = int((self.lower_bound - self.rect.bottom) / self.movement_speed)
                    elif self.vertical_velocity == -1 and self.rect.top + self.vertical_velocity * self.movement_speed * self.direction_length < 0:
                        self.direction_length = int(self.rect.top / self.movement_speed)

            else:
                if self.vertical_velocity == -1:
                    self.horizontal_velocity = 1
                    self.vertical_velocity = 0
                elif self.vertical_velocity == 1:
                    self.horizontal_velocity = -1
                    self.vertical_velocity = 0

            self.rect.x += self.horizontal_velocity * self.movement_speed
            self.rect.y += self.vertical_velocity * self.movement_speed

            if self.rect.right <= 0 or self.rect.left >= self.sc_width:
                self.kill()
