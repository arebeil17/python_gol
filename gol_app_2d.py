import gol_game_pkg.game_control as game_control
from gol_game_pkg.game_constants import InitMode, CellColor
import pygame
import pygame_gui
from pygame import Color, Surface
from pygame.locals import *
import time
import sys
import random
import gol_game_pkg.grid as grid
import gol_game_pkg.game_sprites as game_sprites
from gol_game_pkg.game_types import GameConfig, GameState2D

cell_dim = [20, 20]
window_dim = [1200, 800]
board_init_mode = InitMode.Random
cell_color_mode = CellColor.Colorful
FPS = 2


pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

display_surface = pygame.display.set_mode((window_dim[0], window_dim[1]))
pygame.display.set_caption("Conway's Game of Life")

all_sprites = pygame.sprite.Group()
sprite_map = {}

game_grid = grid.initialize_grid_from_window_size(cell_dim, window_dim)

rows = len(game_grid)
cols = len(game_grid[0])
grid_dim = [cols, rows]

game_state = GameState2D(
    game_grid, 0, FPS, display_surface, all_sprites, sprite_map)

game_config = GameConfig(cell_dim, grid_dim, window_dim, cell_color_mode)

game_state.game_grid = grid.randomize_grid(game_state.game_grid, rows)

game_sprites.initiaize_grid_sprites(game_config, game_state)
# ---------------------------------------------------------
manager = pygame_gui.UIManager((window_dim[0], window_dim[1]), 'menu.json')

background = pygame.Surface((window_dim[0], window_dim[1]))

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window_dim[0] // 2 - 100,
                                            window_dim[1] // 2), (200, 50)),
                                            text='Start Simulation',
                                            manager=manager)

configure_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window_dim[0] // 2 - 100,
                                                window_dim[1] // 2 + 50), (200, 50)),
                                                text='Configure Mode',
                                                manager=manager)

speed_rect = pygame.Rect((window_dim[0] // 2 - 100,
                          window_dim[1] // 2 + 100), (200, 50))

scale_rect = pygame.Rect((window_dim[0] // 2 - 100,
                          window_dim[1] // 2 + 150), (200, 50))

color_rect = pygame.Rect((window_dim[0] // 2 - 100,
                          window_dim[1] // 2 + 200), (200, 50))

fps_setting = 1
scale_setting = 2
color_setting = 1
fps_list = [["slow", 1], ["normal", 2], ["fast", 5], ["ultra", 10]]
scale_list = [["micro", 5, 5], ["small", 10, 10], [
    "normal", 20, 20], ["large", 40, 40], ["Collosal", 80, 80]]
color_list = [["green", 0], ["colorful", 1], ["disco", 2]]
num_speeds = len(fps_list)
num_scales = len(scale_list)
num_colors = len(color_list)

speed_button = pygame_gui.elements.UIButton(speed_rect, text=f'Sim Speed: {fps_list[fps_setting][0]}',
                                            manager=manager)

scale_button = pygame_gui.elements.UIButton(scale_rect, text=f'Cell Size: {scale_list[scale_setting][0]}',
                                            manager=manager)

color_button = pygame_gui.elements.UIButton(color_rect, text=f'Color: {color_list[color_setting][0]}',
                                            manager=manager)

clock = pygame.time.Clock()
is_running = True

while is_running:

    text, text_rect = game_control.create_menu_text_bar(window_dim)

    time_delta = clock.tick(60)/1000.0

    setting_update = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            print("Exiting game!")
            sys.exit(0)

        if event.type == pygame.USEREVENT:

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:

                if event.ui_element == start_button:
                    print('start simulation')
                    board_init_mode = InitMode.Random
                    is_running = False

                if event.ui_element == configure_button:
                    board_init_mode = InitMode.Cursor
                    print('configure mode')
                    is_running = False

                if event.ui_element == speed_button:
                    fps_setting = (fps_setting + 1) % num_speeds
                    pygame_gui.elements.UIButton(speed_rect, text=f'Sim Speed: {fps_list[fps_setting][0]}',
                                                 manager=manager)
                    game_state.fps = fps_list[fps_setting][1]
                    print('Sim Speed: ', {fps_list[fps_setting][0]})

                if event.ui_element == scale_button:
                    scale_setting = (scale_setting + 1) % num_scales
                    pygame_gui.elements.UIButton(scale_rect, text=f'Cell Size: {scale_list[scale_setting][0]}',
                                                 manager=manager)

                    cell_dim = scale_list[scale_setting][1:]
                    print('Scale: ', {scale_list[scale_setting][0]})
                    setting_update = True

                if event.ui_element == color_button:
                    color_setting = (color_setting + 1) % num_colors
                    pygame_gui.elements.UIButton(color_rect, text=f'Color: {color_list[color_setting][0]}',
                                                 manager=manager)

                    game_config.color_mode = color_list[color_setting][1]
                    print('Color Mode: ', {color_list[color_setting][0]})
                    setting_update = True

        manager.process_events(event)

    manager.update(time_delta)

    if setting_update:
        game_sprites.dynamic_grid_sprite_update(
            game_config, game_state, cell_dim, window_dim)

    game_state.display_surface.blit(background, (0, 0))

    game_state.all_sprites.update()
    game_state.display_surface.fill((0, 0, 0))

    for entity in game_state.all_sprites:  # TODO: Make this a function
        game_state.display_surface.blit(entity.outline_surf,
                                        entity.outline_rect)
        game_state.display_surface.blit(entity.cell_surf,
                                        entity.cell_rect)

    manager.draw_ui(game_state.display_surface)
    game_state.display_surface.blit(text, text_rect)

    pygame.display.update()

# ---------------------------------------------------------


game_grid = grid.initialize_grid_from_window_size(cell_dim, window_dim)

rows = len(game_grid)
cols = len(game_grid[0])
grid_dim = [cols, rows]

game_state = GameState2D(
    game_grid, 0, game_state.fps, display_surface, all_sprites, sprite_map)

game_config = GameConfig(
    cell_dim, grid_dim, window_dim, game_config.color_mode)

game_sprites.initiaize_grid_sprites(game_config, game_state)


if InitMode(board_init_mode) == InitMode.Random:
    game_state.game_grid = grid.randomize_grid(game_state.game_grid, rows)
else:
    game_control.cursor_mode_2d(game_config, game_state)

game_control.simualtion_mode_2d(game_config, game_state)
