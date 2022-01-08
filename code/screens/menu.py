import time
import json
import pygame

from code.modules import constants
from code.modules.constants import width, height
from code.screens.game import game
from code.helper_functions.text_helpers import wrap_text, render_text_list


def menu():
    screen, clock, speed = constants.screen, constants.clock, constants.speed
    action = 0  # 0: Menu, 1: Game, 2: Info Guide, -1 (else): Quit

    with open("content/texts.json") as text_json:
        text = json.load(text_json)

    while True:
        if action == 0:
            selection = 1

            title_font = pygame.font.Font('content/fonts/atari.ttf', constants.title_text_height)
            title_text = title_font.render(text["title"], True, constants.primary_text_color)
            button_font = pygame.font.Font('content/fonts/atari.ttf', constants.button_text_height)

            button_texts = [button_font.render(text[name+"_button"], True, constants.secondary_text_color) for name in ["play", "info"]]
            button_height = height//((len(button_texts)+1) * 2)
            button_spacing = (height//2 - (button_height * len(button_texts))) // (len(button_texts) + 1)
            button_spacing = button_spacing if button_spacing > 0 else 0
            button_rects = [pygame.rect.Rect(width//2-button_texts[i].get_width()//2 - width // 15, height//2 + button_spacing * (i + 1) + button_height * i - button_spacing, button_texts[i].get_width() + 2*width//15, button_texts[i].get_height() + button_spacing*2) for i in range(len(button_texts))]

            time.sleep(constants.menu_lag)
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        action = -1
                        break

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            action = -1
                            break

                        if event.key == pygame.K_SPACE:
                            action = selection
                            running = False
                            break

                        if event.key == pygame.K_UP:
                            selection = selection - 1 if selection > 1 else selection

                        if event.key == pygame.K_DOWN:
                            selection = selection + 1 if selection < len(button_texts) else selection

                screen.fill(constants.menu_background_color)
                screen.blit(title_text, (width//2 - title_text.get_width()//2, height//4 - constants.title_text_height//2))
                pygame.draw.rect(screen, constants.selection_color, (button_rects[selection-1].left - width//40, button_rects[selection-1].top - button_spacing//4, button_rects[selection-1].width + width//20, button_rects[selection-1].height + button_spacing//2))
                for button in range(len(button_texts)):
                    pygame.draw.rect(screen, constants.button_color, button_rects[button])
                    screen.blit(button_texts[button], (width//2-button_texts[button].get_width()//2, height//2 + button_spacing * (button + 1) + button_height * button))

                pygame.display.flip()

                clock.tick(speed)

        elif action == 1:
            time.sleep(constants.menu_lag)
            game()
            action = 0
            continue

        elif action == 2:
            height_spacing = height // 20
            width_spacing = width // 20

            box_art = pygame.image.load("content/textures/box_art.jpeg")
            box_art_height = -height_spacing + height // 2
            box_art = pygame.transform.scale(box_art, (box_art.get_width() * box_art_height // box_art.get_height(), box_art_height))

            scores_background_rect = pygame.rect.Rect(width//2 - width_spacing, height//2 + height_spacing, width//2 + width_spacing, height//2 - height_spacing)
            game_objective_background_rect = pygame.rect.Rect(width_spacing, height_spacing, (width//2) - 2 * width_spacing, (height // 2) - height_spacing)
            gameplay_background_rect = pygame.rect.Rect((width//2) + width_spacing, height_spacing, (width//2) - 2*width_spacing, (height//2) - height_spacing)

            scores_font = pygame.font.Font('content/fonts/atari.ttf', constants.info_scores_text_height)
            font = pygame.font.Font('content/fonts/atari.ttf', constants.info_text_height)

            left_scores = [render_text_list(wrap_text(text["scores_left"][i], scores_font, scores_background_rect.width // 2), scores_font, colour=constants.secondary_text_color) for i in range(len(text["scores_left"]))]
            right_scores = [render_text_list(wrap_text(text["scores_right"][i], scores_font, scores_background_rect.width // 2), scores_font, colour=constants.secondary_text_color) for i in range(len(text["scores_right"]))]
            gameplay = [render_text_list(wrap_text(text["gameplay"][i], font, gameplay_background_rect.width), font, colour=constants.secondary_text_color) for i in range(len(text["gameplay"]))]
            game_objective = [render_text_list(wrap_text(text["game_objective_text"][i], font, game_objective_background_rect.width), font, colour=constants.secondary_text_color) for i in range(len(text["game_objective_text"]))]

            time.sleep(constants.menu_lag)

            screen.fill(constants.menu_background_color)

            screen.blit(box_art, (0, height - box_art_height))
            pygame.draw.rect(screen, constants.info_text_background_color, scores_background_rect)
            pygame.draw.rect(screen, constants.info_text_background_color, game_objective_background_rect)
            pygame.draw.rect(screen, constants.info_text_background_color, gameplay_background_rect)

            height_addition = 0
            for text_surf in left_scores:
                screen.blit(text_surf, (scores_background_rect.left, scores_background_rect.top + height_addition))
                height_addition += text_surf.get_height()

            height_addition = 0
            for text_surf in right_scores:
                screen.blit(text_surf, (scores_background_rect.midtop[0], scores_background_rect.top + height_addition))
                height_addition += text_surf.get_height()

            height_addition = 0
            for text_surf in gameplay:
                screen.blit(text_surf, (gameplay_background_rect.left, gameplay_background_rect.top + height_addition))
                height_addition += text_surf.get_height()

            height_addition = 0
            for text_surf in game_objective:
                screen.blit(text_surf, (game_objective_background_rect.left, game_objective_background_rect.top + height_addition))
                height_addition += text_surf.get_height()

            pygame.display.flip()

            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        action = -1
                        break

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                            action = 0
                            break

                clock.tick(speed)

        else:
            break
