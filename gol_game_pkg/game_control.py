from gol_game_pkg.game_types import GameState
import pygame
from pygame import Color, Surface
from pygame.locals import *
import time
import sys
import random
import gol_game_pkg.game_modes as game_modes
import gol_game_pkg.grid as grid
import gol_game_pkg.display as display
from gol_game_pkg.game_constants import CellColor
from gol_game_pkg.game_types import GameState2D, GameConfig
from gol_game_pkg.game_sprites import CellSprite


# HEIGHT = 600
# WIDTH = 1000
ACC = 0.5
FRIC = -0.12


def create_menu_text_bar(window_dim):
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    font = pygame.font.SysFont('Arial', 64)

    text = font.render('Game of Life', True, white, None)

    textRect = text.get_rect()

    textRect.center = (window_dim[0] // 2, (window_dim[1] // 2) // 2)

    return text, textRect


def create_text_bar(window_dim, info_string):
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    font = pygame.font.Font('freesansbold.ttf', 20)

    text = font.render(info_string, True, white, None)

    textRect = text.get_rect()

    textRect.center = (window_dim[0] // 2, window_dim[1] - 20)

    return text, textRect


def cursor_mode_2d(game_config, game_state):

    cursor_mode_fps = 30
    exit_cursor_mode = False
    for entity in game_state.all_sprites:
        game_state.display_surface.blit(entity.outline_surf,
                                        entity.outline_rect)
    while not exit_cursor_mode:
        mouse_up_detected = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_up_detected = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                print("Exiting Cursor mode!")
                exit_cursor_mode = True
                continue

        for y in range(0, game_config.window_dim[1], game_config.cell_dim[1]):
            for x in range(0, game_config.window_dim[0], game_config.cell_dim[0]):
                row = int(y / game_config.cell_dim[0])
                col = int(x / game_config.cell_dim[1])
                is_alive = game_state.game_grid[row][col]
                sprite_key = f'{x},{y}'
                if sprite_key in game_state.sprite_map:
                    cell_sprite = game_state.sprite_map[sprite_key]
                    if mouse_up_detected and cell_sprite.is_clicked():
                        print("Detected clicked sprite at: ", x, ",", y)
                        game_state.game_grid[row][col] = not game_state.game_grid[row][col]
                        is_alive = game_state.game_grid[row][col]
                        print("cell alive: ", is_alive)
                        cell_sprite.update_cell(
                            is_alive, game_config.color_mode)

                if CellColor(game_config.color_mode) == CellColor.Disco:
                    cell_sprite.update_cell(
                        is_alive, game_config.color_mode)

        game_state.all_sprites.update()
        game_state.display_surface.fill((0, 0, 0))

        for entity in game_state.all_sprites:
            # game_state.display_surface.blit(entity.outline_surf,
            #                                 entity.outline_rect)
            game_state.display_surface.blit(entity.cell_surf,
                                            entity.cell_rect)

        pygame.display.flip()

        pygame.time.Clock().tick(cursor_mode_fps)


def simualtion_mode_2d(game_config, game_state):

    simulation_paused = False
    generations = 0
    for entity in game_state.all_sprites:
        game_state.display_surface.blit(entity.outline_surf,
                                        entity.outline_rect)
    while True:
        info_string = f'Generation: {generations} Updates: {game_state.updates}'
        text, text_rect = create_text_bar(game_config.window_dim, info_string)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                print("Simulation toggled Enter key pressed!")
                simulation_paused = not simulation_paused

        if not simulation_paused:

            for y in range(0, game_config.window_dim[1], game_config.cell_dim[1]):
                for x in range(0, game_config.window_dim[0], game_config.cell_dim[0]):
                    row = int(y / game_config.cell_dim[0])
                    col = int(x / game_config.cell_dim[1])

                    sprite_key = f'{x},{y}'
                    if sprite_key in game_state.sprite_map:
                        cell_sprite = game_state.sprite_map[sprite_key]
                        is_alive = game_state.game_grid[row][col]
                        cell_sprite.update_cell(
                            is_alive, game_config.color_mode)

            game_state.all_sprites.update()
            game_state.display_surface.fill((0, 0, 0))

            for entity in game_state.all_sprites:
                # game_state.display_surface.blit(entity.outline_surf,
                #                                 entity.outline_rect)
                game_state.display_surface.blit(entity.cell_surf,
                                                entity.cell_rect)

            game_state.display_surface.blit(text, text_rect)

            game_state = grid.evaluate_grid(
                game_state, game_config.grid_dim[1], game_config.grid_dim[0])

            generations += 1

            pygame.display.flip()

        game_state.all_sprites.remove(text_rect)
        pygame.time.Clock().tick(game_state.fps)
