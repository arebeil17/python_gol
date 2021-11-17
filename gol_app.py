import gol_game_pkg.game_control as game_control
from gol_game_pkg.game_constants import GameMode, CellColor
import pygame
import pygame_gui
from pygame import Color, Surface
from pygame.locals import *
import sys
from gol_game_pkg.game_grid import WindowGrid
import gol_game_pkg.game_sprites as game_sprites
from gol_game_pkg.game_types import GameConfig, GameState2D
from gol_game_pkg.game_gui import GameGui

cell_dim = [20, 20]
window_dim = [1200, 800]
cell_color_mode = CellColor.Default
FPS = 2

pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional

display_surface = pygame.display.set_mode((window_dim[0], window_dim[1]))
pygame.display.set_caption("Conway's Game of Life")

all_sprites = pygame.sprite.Group()
sprite_map = dict()

window_grid = WindowGrid(cell_dim, window_dim)

grid_dim = [window_grid.cols, window_grid.rows]

game_state = GameState2D(
    window_grid, 0, FPS, display_surface, all_sprites, sprite_map)

game_config = GameConfig(cell_dim, window_dim)

game_state.window_grid.randomize_grid()

game_sprites.initiaize_grid_sprites(game_config, game_state)
# ---------------------------------------------------------
manager = pygame_gui.UIManager((window_dim[0], window_dim[1]), 'menu.json')

background = pygame.Surface((window_dim[0], window_dim[1]))

start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((window_dim[0] // 2 - 100,
                                            window_dim[1] // 2), (200, 50)),
                                            text='Start',
                                            manager=manager)

game_gui = GameGui(game_config, manager)

clock = pygame.time.Clock()
is_running = True

for entity in game_state.all_sprites:
    game_state.display_surface.blit(entity.outline_surf,
                                    entity.outline_rect)
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

                    cell_dim = game_config.get_current_selection("scale")[1:]

                if event.ui_element == game_gui.color_button:
                    setting_update = True
                    game_gui.update_setting_button(
                        game_config, "color", game_gui.color_rect)

                    game_config.color_mode = game_config.get_current_selection("color")[
                        1]

        game_gui.manager.process_events(event)

    game_gui.manager.update(time_delta)

    if setting_update:
        game_sprites.dynamic_grid_sprite_update(
            game_config, game_state, cell_dim, window_dim)
        print("cell_dim:", game_config.cell_dim,
              "window_dim:", game_config.window_dim)
        print("rows:", str(game_state.window_grid.rows),
              "cols:", str(game_state.window_grid.cols))

    game_state.display_surface.blit(background, (0, 0))

    game_state.all_sprites.update()
    game_state.display_surface.fill((0, 0, 0))

    for entity in game_state.all_sprites:
        game_state.display_surface.blit(entity.cell_surf,
                                        entity.cell_rect)

    game_gui.manager.draw_ui(game_state.display_surface)
    game_state.display_surface.blit(text, text_rect)

    pygame.display.update()

# ---------------------------------------------------------

if GameMode(game_config.get_current_selection("mode")[1]) == GameMode.Cursor:
    game_sprites.reset_all_sprites_to_dead(
        game_state, game_config)
    game_control.cursor_mode_2d(game_config, game_state)

game_control.simualtion_mode_2d(game_config, game_state)
