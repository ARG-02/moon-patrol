import pygame

import code.modules.constants

vec = pygame.math.Vector2


class Laser(pygame.sprite.Sprite):
    def __init__(self, left, top, buggy_width, sc_width, side=True):
        super(Laser, self).__init__()
        if side:
            self.rect = pygame.rect.Rect(left, top, buggy_width//3, buggy_width//24)
        else:
            self.rect = pygame.rect.Rect(left, top, buggy_width // 12, buggy_width // 6)
        self.side = side
        self.sc_width = sc_width

    def update(self, rocks, ammo, orange_ships, purple_ships, white_ships, alien_lasers):
        self.is_colliding_with_rocks(rocks)
        self.is_colliding_with_ammo(ammo)
        self.is_colliding_with_ship(orange_ships, purple_ships, white_ships)
        self.is_colliding_with_alien_lasers(alien_lasers)

        if self.side:
            self.rect.x += self.rect.w // 2
        else:
            self.rect.y -= self.rect.h // 2

        if self.rect.x >= self.sc_width or self.rect.bottom <= 0:
            self.kill()

    def is_colliding_with_rocks(self, rocks):
        for rock in rocks:
            gets_hit = pygame.sprite.collide_rect(self, rock)
            if gets_hit and not rock.is_dead:
                rock.is_dead = True
                self.kill()
                code.modules.constants.points += 100

    def is_colliding_with_ammo(self, ammo):
        for crate in ammo:
            gets_hit = pygame.sprite.collide_rect(self, crate)
            if gets_hit and not crate.is_dead:
                crate.is_dead = True
                self.kill()

    def is_colliding_with_ship(self, orange_ships, purple_ships, white_ships):
        for ship in orange_ships.sprites() + purple_ships.sprites():
            gets_hit = pygame.sprite.collide_rect(self, ship)
            if gets_hit and not ship.is_dead:
                ship.is_dead = True
                self.kill()
                code.modules.constants.points += 100

        for ship in white_ships.sprites():
            gets_hit = pygame.sprite.collide_rect(self, ship)
            if gets_hit and not ship.is_dead:
                ship.is_dead = True
                self.kill()
                code.modules.constants.points += 200

    def is_colliding_with_alien_lasers(self, alien_lasers):
        for alien_laser in alien_lasers:
            gets_hit = pygame.sprite.collide_rect(self, alien_laser)
            if gets_hit:
                self.kill()
                alien_laser.kill()
