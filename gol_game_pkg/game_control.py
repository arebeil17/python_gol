import pygame
from pygame import Color, Surface
import pygame_gui
from pygame.locals import *
import sys
import gol_game_pkg.display as display
from gol_game_pkg.game_constants import CellColor
from gol_game_pkg.game_types import GameConfig, GameState2D
import gol_game_pkg.game_sprites as game_sprites
from gol_game_pkg.game_grid import WindowGrid


cell_dim = [20, 20]
window_dim = [1200, 800]
FPS = 2


def initialize_game():
    pygame.init()
    vec = pygame.math.Vector2  # 2 for two dimensional

    display_surface = pygame.display.set_mode((window_dim[0], window_dim[1]))
    pygame.display.set_caption("Conway's Game of Life")

    all_sprites = pygame.sprite.Group()
    sprite_map = dict()

    window_grid = WindowGrid(cell_dim, window_dim)

    game_state = GameState2D(
        window_grid, 0, FPS, display_surface, all_sprites, sprite_map)

    game_config = GameConfig(cell_dim, window_dim)

    game_state.window_grid.randomize_grid()

    game_sprites.initiaize_grid_sprites(game_config, game_state)

    return [game_state, game_config]


def run_main_menu(game_gui, game_state, game_config):
    clock = pygame.time.Clock()

    game_sprites.initialize_grid_frame(game_state)

    is_running = True

    while is_running:

        text, text_rect = game_gui.create_menu_text_bar(game_config.window_dim)

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
        game_state.display_surface.blit(text, text_rect)

        pygame.display.update()


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

    simulation_paused = False
    generations = 0
    for entity in game_state.all_sprites:
        game_state.display_surface.blit(entity.outline_surf,
                                        entity.outline_rect)
    while True:
        info_string = f'Generation: {generations} Updates: {game_state.updates}'
        text, text_rect = game_gui.create_text_bar(
            game_config.window_dim, info_string)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                print("Simulation toggled Enter key pressed!")
                simulation_paused = not simulation_paused

        if not simulation_paused:

            game_state.update_all_cell_sprites(game_config)

            for entity in game_state.all_sprites:

                game_state.display_surface.blit(entity.cell_surf,
                                                entity.cell_rect)

            game_state.display_surface.blit(text, text_rect)

            updates = game_state.window_grid.evaluate_grid()
            game_state.updates += updates

            generations += 1

            pygame.display.flip()

        game_state.all_sprites.remove(text_rect)
        pygame.time.Clock().tick(game_state.fps)
