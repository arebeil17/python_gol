import pygame
from gol_game_pkg.game_constants import COLOR_LIST, FPS_LIST, MODE_LIST, SCALE_LIST, DEFAULT_SELECTION_DICT
import gol_game_pkg.game_grid


class GameState:
    def __init__(self, game_grid, updates):
        self.game_grid = game_grid
        self.updates = updates


class GameState2D(GameState):
    def __init__(self, window_grid, updates, fps, display_surface, all_sprites, sprite_map):
        self.window_grid = window_grid
        self.updates = updates
        self.fps = fps
        self.display_surface = display_surface
        self.all_sprites = all_sprites
        self.sprite_map = sprite_map

    def update(self, window_grid, updates, fps, display_surface, all_sprites, sprite_map):
        self.window_grid = window_grid
        self.updates = updates
        self.fps = fps
        self.display_surface = display_surface
        self.all_sprites = all_sprites
        self.sprite_map = sprite_map

    def update_all_cell_sprites(self, game_config):
        for y in range(0, game_config.window_dim[1], game_config.cell_dim[1]):
            for x in range(0, game_config.window_dim[0], game_config.cell_dim[0]):
                row = int(y / game_config.cell_dim[0])
                col = int(x / game_config.cell_dim[1])

                sprite_key = f'{x},{y}'
                if sprite_key in self.sprite_map:
                    cell_sprite = self.sprite_map[sprite_key]
                    is_alive = self.window_grid.grid[row][col]
                    cell_sprite.update_cell(is_alive, game_config.color_mode)

        self.all_sprites.update()
        self.display_surface.fill((0, 0, 0))


class GameConfig:
    def __init__(self, cell_dim, window_dim):
        self.cell_dim = cell_dim
        self.window_dim = window_dim
        self.color_mode = DEFAULT_SELECTION_DICT["color"]
        self.setting_dict = dict()
        self.selection_dict = dict()
        self.selection_dict['mode'] = 0
        self.selection_dict['fps'] = 0
        self.selection_dict['scale'] = 0
        self.selection_dict['color'] = 0

        self.set_setting_lists(MODE_LIST, FPS_LIST,
                               SCALE_LIST, COLOR_LIST, DEFAULT_SELECTION_DICT)

    def set_setting_lists(self, mode_list, fps_list, scale_list, color_list, default_selections_dict):
        self.setting_dict["mode"] = mode_list
        self.setting_dict["fps"] = fps_list
        self.setting_dict["scale"] = scale_list
        self.setting_dict["color"] = color_list
        self.selection_dict['mode'] = default_selections_dict["mode"]
        self.selection_dict['fps'] = default_selections_dict["fps"]
        self.selection_dict['scale'] = default_selections_dict["scale"]
        self.selection_dict['color'] = default_selections_dict["color"]

    def get_current_selection(self, setting_key):
        current_selection = self.selection_dict[setting_key]
        return self.setting_dict[setting_key][current_selection]

    def update(self, cell_dim, window_dim, color_mode):
        self.cell_dim = cell_dim
        self.window_dim = window_dim
        self.color_mode = color_mode
