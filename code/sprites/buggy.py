import pygame

from code.modules import constants

vec = pygame.math.Vector2


class Buggy(pygame.sprite.Sprite):
    def __init__(self, ground, initial_pos):
        super(Buggy, self).__init__()
        self.surfs = [pygame.image.load(f"content/animations/driving_buggy/{i}.png").convert_alpha() for i in range(3)]
        self.surfs = [pygame.transform.scale(i, (constants.buggy_width, self.surfs[0].get_height() * constants.buggy_width // self.surfs[0].get_width())) for i in self.surfs]
        self.rect = self.surfs[0].get_rect()
        self.ground = ground

        self.pos = vec((initial_pos[0], initial_pos[1]-self.rect.height))
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, constants.gravity)
        self.rect.x, self.rect.y = self.pos.x, self.pos.y
        self.frame = 0
        self.ammo = constants.max_ammo

        self.death_surfs = [pygame.image.load(f"content/animations/death/{i}.png").convert_alpha() for i in range(2)]
        self.death_surfs = [pygame.transform.scale(i, (constants.buggy_width, i.get_height() * constants.buggy_width // i.get_width())) for i in self.death_surfs]

        self.death_frame = 0
        self.time_new_frame = 0

    def update_animation(self):
        if self.is_colliding_with_ground():
            self.frame += 1 if self.frame < 2 else -2
        else:
            self.frame = 0

    def move_left(self):
        if constants.width / 8 < self.rect.x and self.is_colliding_with_ground():
            self.pos.x -= self.rect.width // 20

    def move_right(self):
        if 5 * constants.width / 12 > self.rect.right and self.is_colliding_with_ground():
            self.pos.x += self.rect.width // 20

    def move_center(self):
        if self.is_colliding_with_ground():
            if abs(self.rect.centerx - 13 * constants.width // 48) < self.rect.width // 30:
                self.pos.x = constants.width * 13 // 48 - self.rect.w // 2
            else:
                self.pos.x += constants.buggy_centering_speed if self.rect.centerx <= 13 * constants.width // 48 else -constants.buggy_centering_speed

    def update(self, rocks, holes, ammo, alien_lasers):
        if self.is_colliding_with_rocks(rocks) or self.is_colliding_with_holes(holes) or self.is_colliding_with_alien_lasers(alien_lasers):
            self.frame = 0
            return True

        self.jumped_over_holes(holes)
        self.jumped_over_rocks(rocks)

        if self.collect_ammo(ammo):
            self.ammo = min(constants.max_ammo, self.ammo + constants.ammo_crate_amount)

        self.velocity.y += self.acceleration.y
        self.pos.y += self.velocity.y

        self.rect.x, self.rect.y = self.pos.x, self.pos.y
        if self.is_colliding_with_ground():
            self.velocity.y = 0
            self.pos.y = self.ground.top - self.rect.height
            self.rect.y = self.pos.y

    def jumped_over_rocks(self, rocks):
        for rock in rocks.sprites():
            if rock.rect.right < self.rect.left and not rock.has_crossed:
                rock.has_crossed = True
                constants.points += constants.rock_jump_score

    def jumped_over_holes(self, holes):
        for hole in holes.sprites():
            if hole.rect.right < self.rect.left and not hole.has_crossed and not hole.is_created:
                hole.has_crossed = True
                constants.points += constants.hole_jump_score

    def update_death_animation(self):
        self.time_new_frame += 1
        if self.time_new_frame >= 45:
            self.time_new_frame = 0
            self.death_frame += 1
        if self.death_frame > 1:
            self.death_frame = 0
            return None

    def jump(self):
        if self.is_colliding_with_ground():
            self.velocity.y = -constants.buggy_jump_height
            return True

    def is_colliding_with_ground(self):
        collision_rect = self.rect
        collision_rect.y += 1
        col = pygame.Rect.colliderect(self.ground, collision_rect)
        return col

    def is_colliding_with_rocks(self, rocks):
        for rock in rocks:
            gets_hit = pygame.sprite.collide_rect(self, rock)
            if gets_hit and not rock.is_dead:
                return True

    def is_colliding_with_holes(self, holes):
        return pygame.sprite.spritecollideany(self, holes)

    def is_colliding_with_alien_lasers(self, alien_lasers):
        for laser in alien_lasers:
            gets_hit = pygame.sprite.collide_rect(self, laser)
            if gets_hit:
                laser.kill()
                return True

    def collect_ammo(self, ammo):
        for crate in ammo:
            gets_hit = pygame.sprite.collide_rect(self, crate)
            if gets_hit and not crate.is_dead:
                crate.kill()
                crate.kill()
                return True
