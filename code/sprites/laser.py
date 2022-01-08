import pygame

from code.modules import constants

vec = pygame.math.Vector2


class Laser(pygame.sprite.Sprite):
    def __init__(self, left, top, side=True):
        super(Laser, self).__init__()
        if side:
            self.rect = pygame.rect.Rect(left, top, constants.laser_width_horizontal, constants.laser_height_horizontal)
        else:
            self.rect = pygame.rect.Rect(left, top, constants.laser_width_vertical, constants.laser_height_vertical)
        self.side = side

    def update(self, rocks, ammo, orange_ships, purple_ships, white_ships, alien_lasers):
        if self.is_colliding_with_rocks(rocks) or self.is_colliding_with_ammo(ammo):
            return 1
        if self.is_colliding_with_ship(orange_ships, purple_ships, white_ships):
            return 2
        self.is_colliding_with_alien_lasers(alien_lasers)

        if self.side:
            self.rect.x += constants.laser_horizontal_speed
        else:
            self.rect.y -= constants.laser_vertical_speed

        if self.rect.x >= constants.width or self.rect.bottom <= 0:
            self.kill()

    def is_colliding_with_rocks(self, rocks):
        for rock in rocks:
            gets_hit = pygame.sprite.collide_rect(self, rock)
            if gets_hit and not rock.is_dead:
                rock.is_dead = True
                self.kill()
                constants.points += constants.rock_shoot_score
                return True

    def is_colliding_with_ammo(self, ammo):
        for crate in ammo:
            gets_hit = pygame.sprite.collide_rect(self, crate)
            if gets_hit and not crate.is_dead:
                crate.is_dead = True
                self.kill()
                return True

    def is_colliding_with_ship(self, orange_ships, purple_ships, white_ships):
        for ship in orange_ships.sprites():
            gets_hit = pygame.sprite.collide_rect(self, ship)
            if gets_hit and not ship.is_dead:
                ship.is_dead = True
                self.kill()
                constants.points += constants.orange_alien_shoot_score
                return True

        for ship in purple_ships.sprites():
            gets_hit = pygame.sprite.collide_rect(self, ship)
            if gets_hit and not ship.is_dead:
                ship.is_dead = True
                self.kill()
                constants.points += constants.purple_alien_shoot_score
                return True

        for ship in white_ships.sprites():
            gets_hit = pygame.sprite.collide_rect(self, ship)
            if gets_hit and not ship.is_dead:
                ship.is_dead = True
                self.kill()
                constants.points += constants.white_alien_shoot_score
                return True

    def is_colliding_with_alien_lasers(self, alien_lasers):
        for alien_laser in alien_lasers:
            gets_hit = pygame.sprite.collide_rect(self, alien_laser)
            if gets_hit:
                self.kill()
                alien_laser.kill()
