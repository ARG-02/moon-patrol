import random
import pygame
from time import sleep

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
from code.sprites.white_ship import WhiteShip
from code.modules.constants import width, height
from code.modules import constants


def game():
    screen, clock, speed, left_model, right_model = constants.screen, constants.clock, constants.speed, constants.left_model, constants.right_model

    pygame.mixer.music.load("content/sounds/background_music.mp3")
    pygame.mixer.music.set_volume(2)
    font = pygame.font.Font('content/fonts/atari.ttf', constants.secondary_text_height)

    buggy_death = pygame.mixer.Sound("content/sounds/buggy_death.mp3")
    destroy = pygame.mixer.Sound("content/sounds/destroy.mp3")
    jump = pygame.mixer.Sound("content/sounds/jump.mp3")
    kill_alien = pygame.mixer.Sound("content/sounds/kill_alien.mp3")
    shoot = pygame.mixer.Sound("content/sounds/shoot.mp3")
    spawn_alien = pygame.mixer.Sound("content/sounds/spawn_alien.mp3")

    ground = pygame.Rect(0, height*5//6 - constants.ground_height, width, constants.ground_height)

    panel_text_spacing = ((height - ground.bottom) - (font.get_height() * 2)) // 3
    panel_text_spacing = panel_text_spacing if panel_text_spacing > 0 else 0

    lives = constants.lives
    time = 0
    life_bonus_requirement = constants.life_bonus_requirement

    while lives >= 0:
        # initialize all sprites & groups
        buggy = Buggy(ground, (width // 5, ground.top))
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

        mountains.add(Mountain(0, ground))
        mountains.add(Mountain(width, ground))

        # Manually add some stars at start of round
        for generate_star in range(random.randint(10, 30)):
            stars.add(Star(random.randint(0, ground.top), random.randint(0, width), random.choice(constants.star_colors)))

        left_is_pressed = 0

        pygame.mixer.music.play(loops=-1)

        # Get text for how many lives the player has
        lives_text = font.render(str(lives), True, constants.primary_text_color)

        update_animations = pygame.USEREVENT + constants.user_events
        constants.user_events += 1
        pygame.time.set_timer(update_animations, constants.update_animations_time)

        rock_time = pygame.USEREVENT + constants.user_events
        pygame.time.set_timer(rock_time, random.randint(constants.initial_rock_spawn_time[0], constants.initial_rock_spawn_time[1]), loops=1)
        constants.user_events += 1

        hole_time = pygame.USEREVENT + constants.user_events
        pygame.time.set_timer(hole_time, random.randint(constants.initial_hole_spawn_time[0], constants.initial_hole_spawn_time[1]), loops=1)
        constants.user_events += 1

        ammo_time = pygame.USEREVENT + constants.user_events
        pygame.time.set_timer(ammo_time, random.randint(constants.initial_ammo_spawn_time[0], constants.initial_ammo_spawn_time[1]), loops=1)
        constants.user_events += 1

        time_bonus = pygame.USEREVENT + constants.user_events

        pygame.time.set_timer(time_bonus, constants.bonus_time, loops=-1)
        constants.user_events += 1

        time_counter = pygame.USEREVENT + constants.user_events

        pygame.time.set_timer(time_counter, 1000, loops=-1)
        constants.user_events += 1

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

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        lives = -1
                        break
                    # if event.key == pygame.K_UP:
                    #     if buggy.jump():
                    #         jump.play()
                    # if event.key == pygame.K_SPACE:
                    #     if buggy.ammo > 0 and len(lasers.sprites()) < constants.max_buggy_shoot_amount:
                    #         buggy.ammo = buggy.ammo - 2 if buggy.ammo >= 2 else 0
                    #         lasers.add(Laser(buggy.rect.right, buggy.rect.top + buggy.rect.height // 2))
                    #         lasers.add(Laser(buggy.rect.left + buggy.rect.width // 3, buggy.rect.top - buggy.rect.height, side=False))
                    #         shoot.play()

                if event.type == rock_time:
                    rocks.add(Rock(width, ground.top))

                    rock_time = pygame.USEREVENT + constants.user_events
                    pygame.time.set_timer(rock_time, random.randint(constants.rock_spawn_rate[0], constants.rock_spawn_rate[1]), loops=1)
                    constants.user_events += 1

                if event.type == hole_time:
                    holes.add(Hole(width, ground.top))

                    hole_time = pygame.USEREVENT + constants.user_events
                    pygame.time.set_timer(hole_time, random.randint(constants.hole_spawn_rate[0], constants.hole_spawn_rate[1]), loops=1)
                    constants.user_events += 1

                if event.type == ammo_time:
                    ammo.add(Ammo(width, ground.top))

                    ammo_time = pygame.USEREVENT + constants.user_events
                    pygame.time.set_timer(ammo_time, random.randint(constants.ammo_spawn_rate[0], constants.ammo_spawn_rate[1]), loops=1)
                    constants.user_events += 1

                if event.type == time_counter:
                    time += 1

                if event.type == time_bonus:
                    constants.points += constants.time_bonus_amount

            if constants.webcam_data[2][0] > 0.95:
                if constants.webcam_data[1][0] != left_is_pressed and constants.webcam_data[1][0] == 1:  # Shoot
                    if buggy.ammo > 0 and len(lasers.sprites()) < constants.max_buggy_shoot_amount:
                        buggy.ammo = buggy.ammo - 2 if buggy.ammo >= 2 else 0
                        lasers.add(Laser(buggy.rect.right, buggy.rect.top + buggy.rect.height // 2))
                        lasers.add(Laser(buggy.rect.left + buggy.rect.width // 3, buggy.rect.top - buggy.rect.height, side=False))
                        shoot.play()
                if constants.webcam_data[1][0] != left_is_pressed and constants.webcam_data[1][0] == 2:  # Jump
                    if buggy.jump():
                        jump.play()
                left_is_pressed = constants.webcam_data[1][0]
            if constants.webcam_data[2][1] > 0.95:
                if constants.webcam_data[1][1] == 1:
                    buggy.move_left()
                elif constants.webcam_data[1][1] == 2:
                    buggy.move_right()
                else:
                    buggy.move_center()

            ammo_text = font.render(str(buggy.ammo), True, constants.primary_text_color)
            score_text = font.render(str(constants.points), True, constants.primary_text_color)
            time_text = font.render(f"{time//60}:{'0' + str(time%60) if time%60 < 10 else str(time%60)}", True, constants.primary_text_color)

            if random.random() < constants.star_spawn_rate:
                stars.add(Star(random.randint(0, ground.top), width, random.choice(constants.star_colors)))

            if random.random() < constants.orange_alien_spawn_rate:
                orange_ships.add(OrangeShip(ground,
                                            random.randint(9, 12),
                                            mountains.sprites()[0].rect.top)
                                 )
                spawn_alien.play()
            if random.random() < constants.purple_alien_spawn_rate:
                purple_ships.add(PurpleShip(ground,
                                            random.randint(9, 12),
                                            mountains.sprites()[0].rect.top)
                                 )
                spawn_alien.play()
            if random.random() < constants.white_alien_spawn_rate:
                white_ships.add(WhiteShip(ground,
                                            random.randint(9, 12),
                                            mountains.sprites()[0].rect.top)
                                 )
                spawn_alien.play()

            if random.random() < constants.orange_alien_shoot_rate:
                if orange_ships.sprites():
                    orange_ship = random.choice(orange_ships.sprites())
                    alien_lasers.add(AlienLaser(orange_ship.rect.midbottom, variant=0))
            if random.random() < constants.purple_alien_shoot_rate:
                if purple_ships.sprites():
                    purple_ship = random.choice(purple_ships.sprites())
                    alien_lasers.add(AlienLaser(purple_ship.rect.midbottom, variant=1))
            if random.random() < constants.white_alien_shoot_rate:
                if white_ships.sprites():
                    white_ship = random.choice(white_ships.sprites())
                    alien_lasers.add(AlienLaser(white_ship.rect.midbottom, variant=2))

            if constants.points >= life_bonus_requirement:
                life_bonus_requirement += constants.life_bonus_requirement
                lives += 1
                lives_text = font.render(str(lives), True, constants.primary_text_color)

            if buggy.update(rocks, holes, ammo, alien_lasers):
                round_running = True

                pygame.mixer.music.stop()
                buggy_death.play()

                end_round = pygame.USEREVENT + constants.user_events
                pygame.time.set_timer(end_round, int(1000*buggy_death.get_length()) + constants.death_length, loops=1)
                constants.user_events += 1

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
                    for laser in lasers:
                        update = laser.update(rocks, ammo, orange_ships, purple_ships, white_ships, alien_lasers)
                        if update == 1:
                            destroy.play()
                        elif update == 2:
                            kill_alien.play()
                    buggy.update_death_animation()

                    for alien_laser in alien_lasers:
                        if alien_laser.update(ground):
                            if alien_laser.rect.midbottom[0] < buggy.rect.left:
                                holes.add(Hole(alien_laser.rect.midtop[0] - constants.hole_width // 2, ground.top,
                                               is_created=True))
                            else:
                                holes.add(Hole(alien_laser.rect.midtop[0] - constants.hole_width // 2, ground.top))
                            alien_laser.kill()
                    for crate in ammo.sprites():
                        crate.update_death_animation()
                    for rock in rocks.sprites():
                        rock.update_death_animation()

                    screen.fill(constants.sky_color)
                    for star in stars.sprites():
                        pygame.draw.rect(screen, star.color, star.rect)
                    pygame.draw.rect(screen, constants.ground_color, ground)
                    for mountain in mountains.sprites():
                        screen.blit(mountain.surf, mountain.rect)
                    for ship in orange_ships.sprites():
                        screen.blit(ship.surfs[ship.frame], ship.rect)
                    for ship in purple_ships.sprites():
                        screen.blit(ship.surfs[ship.frame], ship.rect)
                    for ship in white_ships.sprites():
                        screen.blit(ship.surfs[ship.frame], ship.rect)
                    for laser in lasers.sprites():
                        pygame.draw.rect(screen, constants.laser_color, laser.rect)
                    for hole in holes.sprites():
                        screen.blit(hole.surf, hole.rect)
                    screen.blit(buggy.death_surfs[buggy.death_frame], buggy.rect)
                    for ammo_crate in ammo.sprites():
                        screen.blit(ammo_crate.surf, ammo_crate.rect)
                    for rock in rocks.sprites():
                        screen.blit(rock.surf, rock.rect)
                    screen.blit(ammo_text, (width*2//5 - ammo_text.get_width() // 2, height * 5 // 6 + panel_text_spacing))
                    screen.blit(score_text, (width*2//5 - score_text.get_width() // 2, height * 11 // 12 + panel_text_spacing))
                    screen.blit(time_text, (width*3//5 - time_text.get_width() // 2, height * 5 // 6 + panel_text_spacing))
                    screen.blit(lives_text, (width * 3//5 - lives_text.get_width() // 2, height * 11 // 12 + panel_text_spacing))

                    pygame.display.flip()

                    clock.tick(speed)

                lives -= 1
                running = False
                sleep(0.5)
                break

            for laser in lasers:
                update = laser.update(rocks, ammo, orange_ships, purple_ships, white_ships, alien_lasers)
                if update == 1:
                    destroy.play()
                elif update == 2:
                    kill_alien.play()
            stars.update()
            for mountain in mountains:
                if mountain.update():
                    mountains.add(Mountain(width+mountain.rect.right, ground))
                    mountains.sprites()[-1].update()
            rocks.update()
            holes.update()
            ammo.update()
            orange_ships.update()
            purple_ships.update()
            white_ships.update()
            for alien_laser in alien_lasers:
                if alien_laser.update(ground):
                    if alien_laser.rect.midbottom[0] < buggy.rect.left:
                        holes.add(Hole(alien_laser.rect.midtop[0] - constants.hole_width//2, ground.top, is_created=True))
                    else:
                        holes.add(Hole(alien_laser.rect.midtop[0] - constants.hole_width//2, ground.top))
                    alien_laser.kill()
            screen.fill(constants.sky_color)
            for star in stars.sprites():
                pygame.draw.rect(screen, star.color, star.rect)
            pygame.draw.rect(screen, constants.ground_color, ground)
            for mountain in mountains.sprites():
                screen.blit(mountain.surf, mountain.rect)
            for ship in orange_ships.sprites():
                screen.blit(ship.surf, ship.rect)
            for ship in purple_ships.sprites():
                screen.blit(ship.surf, ship.rect)
            for ship in white_ships.sprites():
                screen.blit(ship.surf, ship.rect)
            for laser in lasers.sprites():
                pygame.draw.rect(screen, constants.laser_color, laser.rect)
            for hole in holes.sprites():
                screen.blit(hole.surf, hole.rect)
            screen.blit(buggy.surfs[buggy.frame], buggy.rect)
            for ammo_crate in ammo.sprites():
                screen.blit(ammo_crate.surf, ammo_crate.rect)
            for rock in rocks.sprites():
                screen.blit(rock.surf, rock.rect)
            for alien_laser in alien_lasers.sprites():
                pygame.draw.rect(screen, constants.alien_laser_color, alien_laser.rect)

            screen.blit(constants.webcam_data[0][0], (0, height - constants.webcam_data[0][0].get_height()))
            screen.blit(constants.webcam_data[0][1], (width - constants.webcam_data[0][1].get_width(), height - constants.webcam_data[0][1].get_height()))
            screen.blit(ammo_text, (width * 2 // 5 - ammo_text.get_width() // 2, height * 5 // 6 + panel_text_spacing))
            screen.blit(score_text, (width * 2 // 5 - score_text.get_width() // 2, height * 11 // 12 + panel_text_spacing))
            screen.blit(time_text, (width * 3 // 5 - time_text.get_width() // 2, height * 5 // 6 + panel_text_spacing))
            screen.blit(lives_text, (width * 3 // 5 - lives_text.get_width() // 2, height * 11 // 12 + panel_text_spacing))

            pygame.display.flip()

            clock.tick(speed)

    pygame.mixer.music.stop()
