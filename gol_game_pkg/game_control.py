import pygame
from pygame import Color, Surface
import pygame_gui
from pygame.locals import *
import sys
from gol_game_pkg.game_constants import CellColor
from gol_game_pkg.game_types import GameConfig, GameState2D
import gol_game_pkg.game_sprites as game_sprites
from gol_game_pkg.game_grid import WindowGrid
import gol_game_pkg.game_constants as game_constants


def initialize_game():

    window_dim = game_constants.DEFAULT_WINDOW_DIM
    cell_dim = game_constants.DEFAULT_CELL_DIM
    frames_per_sec = game_constants.DEFAULT_FPS

    pygame.init()
    vec = pygame.math.Vector2  # 2 for two dimensional

    display_surface = pygame.display.set_mode((window_dim[0], window_dim[1]))
    pygame.display.set_caption("Conway's Game of Life")

    all_sprites = pygame.sprite.Group()
    sprite_map = dict()

    window_grid = WindowGrid(cell_dim, window_dim)

    game_state = GameState2D(
        window_grid, 0, frames_per_sec, display_surface, all_sprites, sprite_map)

    game_config = GameConfig(cell_dim, window_dim)

    game_state.window_grid.randomize_grid()

    game_sprites.initiaize_grid_sprites(game_config, game_state)

    return [game_state, game_config]


def run_main_menu(game_gui, game_state, game_config):
    clock = pygame.time.Clock()

    game_sprites.initialize_grid_frame(game_state)

    is_running = True

    while is_running:

        time_delta = clock.tick(60)/1000.0

        setting_update = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                print("Exiting game!")
                sys.exit(0)

            if event.type == pygame.USEREVENT:

                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:

                    if event.ui_element == game_gui.start_button:
                        print('start simulation')
                        is_running = False

                    if event.ui_element == game_gui.mode_button:
                        game_gui.update_setting_button(
                            game_config, "mode", game_gui.mode_rect)

                    if event.ui_element == game_gui.speed_button:
                        game_gui.update_setting_button(
                            game_config, "fps", game_gui.speed_rect)

                        game_state.fps = game_config.get_current_selection("fps")[
                            1]

                    if event.ui_element == game_gui.scale_button:
                        setting_update = True
                        game_gui.update_setting_button(
                            game_config, "scale", game_gui.scale_rect)

                        game_config.cell_dim = game_config.get_current_selection("scale")[
                            1:]

                    if event.ui_element == game_gui.color_button:
                        setting_update = True
                        game_gui.update_setting_button(
                            game_config, "color", game_gui.color_rect)

                        game_config.color_mode = game_config.get_current_selection("color")[
                            1]

            game_gui.manager.process_events(event)

        game_gui.manager.update(time_delta)

        if setting_update:
            game_sprites.dynamic_grid_sprite_update(game_config, game_state)

        game_state.display_surface.blit(game_gui.background, (0, 0))

        game_state.all_sprites.update()
        game_state.display_surface.fill((0, 0, 0))

        for entity in game_state.all_sprites:
            game_state.display_surface.blit(entity.cell_surf,
                                            entity.cell_rect)

        game_gui.manager.draw_ui(game_state.display_surface)

        text1, text_rect1 = game_gui.create_title_text_bar(
            game_config.window_dim)

        text2, text_rect2 = game_gui.create_title_outline_text_bar(
            game_config.window_dim, text_rect1)

        game_state.display_surface.blit(text2, text_rect2)
        game_state.display_surface.blit(text1, text_rect1)

        pygame.display.update()


def cursor_mode_2d(game_config, game_state):

    cursor_mode_fps = 30
    exit_cursor_mode = False
    game_sprites.initialize_grid_frame(game_state)

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
                is_alive = game_state.window_grid.grid[row][col]
                sprite_key = f'{x},{y}'
                if sprite_key in game_state.sprite_map:
                    cell_sprite = game_state.sprite_map[sprite_key]
                    if mouse_up_detected and cell_sprite.is_clicked():
                        print("Detected clicked sprite at: ", x, ",", y)
                        game_state.window_grid.grid[row][col] = not game_state.window_grid.grid[row][col]
                        is_alive = game_state.window_grid.grid[row][col]
                        print("cell alive: ", is_alive)
                        cell_sprite.update_cell(
                            is_alive, game_config.color_mode)

                if CellColor(game_config.color_mode) == CellColor.Disco:
                    cell_sprite.update_cell(
                        is_alive, game_config.color_mode)

        game_state.all_sprites.update()
        game_state.display_surface.fill((0, 0, 0))

        for entity in game_state.all_sprites:
            game_state.display_surface.blit(entity.cell_surf,
                                            entity.cell_rect)

        pygame.display.flip()

        pygame.time.Clock().tick(cursor_mode_fps)


def simualtion_mode_2d(game_gui, game_config, game_state):
    cell_growth_in_progress = True
    simulation_paused = False
    generations = 0
    updates = 0

    game_sprites.initialize_grid_frame(game_state)

    while True:
        prev_updates = updates

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                print("Simulation toggled Enter key pressed!")
                simulation_paused = not simulation_paused

        game_state.update_all_cell_sprites(game_config)
        for entity in game_state.all_sprites:
            game_state.display_surface.blit(entity.cell_surf,
                                            entity.cell_rect)

        if not simulation_paused and cell_growth_in_progress:

            info_string = f'Generations: {generations} Updates: {game_state.updates} Status: {"ACTIVE"}'
            text, text_rect = game_gui.create_text_bar(game_config.window_dim,
                                                       info_string)

            updates = game_state.window_grid.evaluate_grid()
            game_state.updates += updates

            generations += 1

        else:
            info_string = f'Generations: {generations} Updates: {game_state.updates} Status: {"PAUSED" if simulation_paused else "INACTIVE"}'
            text, text_rect = game_gui.create_text_bar(game_config.window_dim,
                                                       info_string)
        game_state.display_surface.blit(text, text_rect)
        pygame.display.flip()

        game_state.all_sprites.remove(text_rect)
        pygame.time.Clock().tick(game_state.fps)

        if prev_updates == game_state.updates:
            cell_growth_in_progress = False
