import random

import pygame
from pygame import KEYDOWN

from code.sprites.alien_laser import AlienLaser
from code.sprites.ammo import Ammo
from code.sprites.buggy import Buggy
from code.sprites.hole import Hole
from code.sprites.laser import Laser
from code.sprites.mountain import Mountain
from code.sprites.orange_ship import OrangeShip
from code.sprites.purple_ship import PurpleShip
from code.sprites.rock import Rock
from code.sprites.star import Star
from code.modules.constants import width, height, init
from code.modules import constants
from code.sprites.white_ship import WhiteShip

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Green Beans")
init()

screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
speed = 60

pygame.mixer.music.load("content/sounds/background_music.mp3")

ground = pygame.Rect(0, height * 3 // 4, width, height // 12)

buggy_ex = pygame.image.load(f"content/animations/driving_buggy/0.png")
buggy_width = width // 15
buggy_height = buggy_ex.get_height() * buggy_width // buggy_ex.get_width()
initial_pos = (width // 5, ground.top - buggy_height)

buggy = Buggy(ground, buggy_width, buggy_height, initial_pos, width)
lasers = pygame.sprite.Group()
stars = pygame.sprite.Group()
mountains = pygame.sprite.Group()
rocks = pygame.sprite.Group()
holes = pygame.sprite.Group()
ammo = pygame.sprite.Group()
orange_ships = pygame.sprite.Group()
purple_ships = pygame.sprite.Group()
white_ships = pygame.sprite.Group()
alien_lasers = pygame.sprite.Group()

font = pygame.font.Font('content/fonts/bit5x3.ttf', height // 12)

star_colors = [
    (125, 176, 76),
    (176, 144, 56),
    (109, 80, 202),
    (248, 248, 71),
    (234, 124, 126)
]

user_events = 0
update_animations = pygame.USEREVENT + user_events
user_events += 1
pygame.time.set_timer(update_animations, 100)

mountains.add(Mountain(0, width, ground))
mountains.add(Mountain(width, width, ground))

for generate_star in range(random.randint(10, 30)):
    stars.add(Star(random.randint(0, ground.top), random.randint(0, width), width, random.choice(star_colors)))

lives = 3

rock_times = []

rock_times.append(pygame.USEREVENT + user_events)
pygame.time.set_timer(rock_times[-1], random.randint(5000, 8000), loops=1)
user_events += 1

hole_times = []

hole_times.append(pygame.USEREVENT + user_events)
pygame.time.set_timer(hole_times[-1], random.randint(4000, 7000), loops=1)
user_events += 1

ammo_times = []

ammo_times.append(pygame.USEREVENT + user_events)
pygame.time.set_timer(ammo_times[-1], random.randint(25000, 30000), loops=1)
user_events += 1

time = 0
time_counter = pygame.USEREVENT + user_events

pygame.time.set_timer(time_counter, 1000, loops=-1)
user_events += 1

time_bonus = pygame.USEREVENT + user_events

pygame.time.set_timer(time_bonus, 30000, loops=-1)
user_events += 1

pygame.mixer.music.play(loops=-1)


while lives >= 0:
    lives_text = font.render(str(lives), True, (184, 156, 88))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == update_animations:
                buggy.update_animation()
                for ship in orange_ships.sprites() + purple_ships.sprites() + white_ships.sprites():
                    ship.update_animation()

            if event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                    break
                if event.key == pygame.K_UP:
                    buggy.jump()
                if event.key == pygame.K_SPACE:
                    if buggy.ammo > 0 and len(lasers.sprites()) < 5:
                        buggy.ammo -= 2
                        lasers.add(Laser(buggy.rect.right, buggy.rect.top + buggy.rect.height // 2, buggy.rect.width, width))
                        lasers.add(Laser(buggy.rect.left + buggy.rect.width // 3, buggy.rect.top - buggy.rect.height, buggy.rect.width, width, side=False))

            if event.type in rock_times:
                rocks.add(Rock(width, ground.top, width * 3//80))

                rock_times.append(pygame.USEREVENT + user_events)
                pygame.time.set_timer(rock_times[-1], random.randint(2000, 8000), loops=1)
                user_events += 1

            if event.type in hole_times:
                holes.add(Hole(width, ground.top, width//20))

                hole_times.append(pygame.USEREVENT + user_events)
                pygame.time.set_timer(hole_times[-1], random.randint(2000, 8000), loops=1)
                user_events += 1

            if event.type in ammo_times:
                ammo.add(Ammo(width, ground.top, width//30))

                ammo_times.append(pygame.USEREVENT + user_events)
                pygame.time.set_timer(ammo_times[-1], random.randint(20000, 25000), loops=1)
                user_events += 1

            if event.type == time_counter:
                time += 1

            if event.type == time_bonus:
                constants.points += 500

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            buggy.move_left()
        elif keys[pygame.K_RIGHT]:
            buggy.move_right()
        else:
            buggy.move_center()

        ammo_text = font.render(str(buggy.ammo), True, (184, 156, 88))
        score_text = font.render(str(constants.points), True, (184, 156, 88))
        time_text = font.render(f"{time//60}:{'0' + str(time%60) if time%60 < 10 else str(time%60)}", True, (184, 156, 88))

        if random.random() < 0.02:
            stars.add(Star(random.randint(0, ground.top), width, width, random.choice(star_colors)))

        if random.random() < 0.002:
            orange_ships.add(OrangeShip(ground, width // 20, (random.choice((-width//20, width)),
                                                              random.randint(0, mountains.sprites()[
                                                                  0].rect.top - width * 7 // 480)),
                                        (width, height), random.randint(9, 12), mountains.sprites()[0].rect.top))
        if random.random() < 0.0015:
            purple_ships.add(PurpleShip(ground, width // 20, (random.choice((-width // 20, width)),
                                                              random.randint(0, mountains.sprites()[
                                                                  0].rect.top - width * 7 // 480)),
                                        (width, height), random.randint(9, 12), mountains.sprites()[0].rect.top))
        if random.random() < 0.0015:
            white_ships.add(WhiteShip(ground, width // 20, (random.choice((-width // 20, width)),
                                      random.randint(0, mountains.sprites()[0].rect.top - width * 7 // 480)),
                                        (width, height), random.randint(9, 12), mountains.sprites()[0].rect.top))

        if random.random() < 0.01:
            if orange_ships.sprites():
                orange_ship = random.choice(orange_ships.sprites())
                alien_lasers.add(AlienLaser(orange_ship.rect.midbottom, buggy.rect.width, width, type=0))
        if random.random() < 0.02:
            if purple_ships.sprites():
                purple_ship = random.choice(purple_ships.sprites())
                alien_lasers.add(AlienLaser(purple_ship.rect.midbottom, buggy.rect.width, width, type=1))
        if random.random() < 0.005:
            if white_ships.sprites():
                white_ship = random.choice(white_ships.sprites())
                alien_lasers.add(AlienLaser(white_ship.rect.midbottom, buggy.rect.width, width, type=2))

        if len(mountains) < 2:
            mountains.add(Mountain(width, width, ground))

        if buggy.update(rocks, holes, ammo, alien_lasers):
            end_round = pygame.USEREVENT + user_events
            pygame.time.set_timer(end_round, 4000, loops=1)
            user_events += 1
            round_running = True
            pygame.mixer.music.stop()
            while round_running:
                for event in pygame.event.get():
                    if event.type == end_round:
                        round_running = False
                        break
                    if event.type == update_animations:
                        for ship in orange_ships.sprites() + purple_ships.sprites() + white_ships.sprites():
                            ship.update_animation()

                orange_ships.update()
                purple_ships.update()
                white_ships.update()
                buggy.update_death_animation()
                lasers.update(rocks, ammo, orange_ships, purple_ships, white_ships, alien_lasers)
                for alien_laser in alien_lasers:
                    if alien_laser.update(ground):
                        holes.add(Hole(alien_laser.rect.midtop[0] - width//40, ground.top, width // 20))
                for crate in ammo.sprites():
                    crate.update_death_animation()
                for rock in rocks.sprites():
                    rock.update_death_animation()

                screen.fill((0, 0, 0))
                for star in stars.sprites():
                    pygame.draw.rect(screen, star.color, star.rect)
                pygame.draw.rect(screen, (108, 152, 80), ground)
                for mountain in mountains.sprites():
                    screen.blit(mountain.surf, mountain.rect)
                for ship in orange_ships.sprites():
                    screen.blit(ship.surfs[ship.frame], ship.rect)
                for ship in purple_ships.sprites():
                    screen.blit(ship.surfs[ship.frame], ship.rect)
                for ship in white_ships.sprites():
                    screen.blit(ship.surfs[ship.frame], ship.rect)
                for laser in lasers.sprites():
                    pygame.draw.rect(screen, (213, 204, 75), laser.rect)
                screen.blit(buggy.death_surfs[buggy.death_frame], buggy.rect)
                for ammo_crate in ammo.sprites():
                    screen.blit(ammo_crate.surf, ammo_crate.rect)
                for hole in holes.sprites():
                    screen.blit(hole.surf, hole.rect)
                for rock in rocks.sprites():
                    screen.blit(rock.surf, rock.rect)
                screen.blit(ammo_text, (width*2//5 - ammo_text.get_width() // 2, height * 5 // 6))
                screen.blit(score_text, (width*2//5 - score_text.get_width() // 2, height * 11 // 12))
                screen.blit(time_text, (width*3//5 - time_text.get_width() // 2, height * 5 // 6))
                screen.blit(lives_text, (width * 3//5 - lives_text.get_width() // 2, height * 11 // 12))

                pygame.display.flip()

                clock.tick(speed)

            lives -= 1
            running = False
            break

        lasers.update(rocks, ammo, orange_ships, purple_ships, white_ships, alien_lasers)
        stars.update()
        mountains.update()
        rocks.update()
        holes.update()
        ammo.update()
        orange_ships.update()
        purple_ships.update()
        white_ships.update()
        for alien_laser in alien_lasers:
            if alien_laser.update(ground):
                holes.add(Hole(alien_laser.rect.midtop[0] - width // 40, ground.top, width // 20))
                alien_laser.kill()

        screen.fill((0, 0, 0))
        for star in stars.sprites():
            pygame.draw.rect(screen, star.color, star.rect)
        pygame.draw.rect(screen, (108, 152, 80), ground)
        for mountain in mountains.sprites():
            screen.blit(mountain.surf, mountain.rect)
        for ship in orange_ships.sprites():
            screen.blit(ship.surf, ship.rect)
        for ship in purple_ships.sprites():
            screen.blit(ship.surf, ship.rect)
        for ship in white_ships.sprites():
            screen.blit(ship.surf, ship.rect)
        for laser in lasers.sprites():
            pygame.draw.rect(screen, (213, 204, 75), laser.rect)
        screen.blit(buggy.surfs[buggy.frame], buggy.rect)
        for ammo_crate in ammo.sprites():
            screen.blit(ammo_crate.surf, ammo_crate.rect)
        for hole in holes.sprites():
            screen.blit(hole.surf, hole.rect)
        for rock in rocks.sprites():
            screen.blit(rock.surf, rock.rect)
        for alien_laser in alien_lasers.sprites():
            pygame.draw.rect(screen, (213, 204, 75), alien_laser.rect)
        screen.blit(ammo_text, (width * 2 // 5 - ammo_text.get_width() // 2, height * 5 // 6))
        screen.blit(score_text, (width * 2 // 5 - score_text.get_width() // 2, height * 11 // 12))
        screen.blit(time_text, (width * 3 // 5 - time_text.get_width() // 2, height * 5 // 6))
        screen.blit(lives_text, (width * 3 // 5 - lives_text.get_width() // 2, height * 11 // 12))

        pygame.display.flip()

        clock.tick(speed)
