import pygame
from pygame import Color, Surface
from pygame.locals import *
import random
from gol_game_pkg.game_constants import CELL_COLORS, GAME_COLORS
from gol_game_pkg.game_constants import CellColor
from gol_game_pkg.game_grid import WindowGrid
from gol_game_pkg.game_types import GameConfig, GameState2D


class CellSprite(pygame.sprite.Sprite):
    def __init__(self,  pos, cell_dim, is_alive, color_mode):
        super().__init__()
        grid_line_dim = 1
        self.outline_surf = pygame.Surface((cell_dim[0], cell_dim[1]))
        self.outline_surf.fill(GAME_COLORS["BLACK"])
        self.cell_surf = pygame.Surface(
            (cell_dim[0] - grid_line_dim, cell_dim[1] - grid_line_dim))
        self.random_color = random.choice(list(CELL_COLORS.values()))
        if is_alive:
            if CellColor(color_mode) == CellColor.Disco or CellColor(color_mode) == CellColor.Colorful:
                self.cell_surf.fill(self.random_color)
            else:
                self.cell_surf.fill(GAME_COLORS["MATRIX_GREEN"])
        else:
            self.cell_surf.fill(GAME_COLORS["GRAY"])

        self.outline_rect = self.outline_surf.get_rect(center=(pos[0], pos[1]))
        self.cell_rect = self.cell_surf.get_rect(center=(pos[0], pos[1]))

    def update_cell(self, is_alive, color_mode):
        if is_alive:
            if CellColor(color_mode) == CellColor.Disco:
                random_color = random.choice(list(CELL_COLORS.values()))
                self.cell_surf.fill(random_color)
            elif CellColor(color_mode) == CellColor.Colorful:
                self.cell_surf.fill(self.random_color)
            else:
                self.cell_surf.fill(GAME_COLORS["MATRIX_GREEN"])
        else:
            self.cell_surf.fill(GAME_COLORS["GRAY"])

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.cell_rect.collidepoint(pygame.mouse.get_pos())


def initiaize_grid_sprites(game_config, game_state):
    for y in range(0, game_config.window_dim[1], game_config.cell_dim[1]):
        for x in range(0, game_config.window_dim[0], game_config.cell_dim[0]):
            row = int(y / game_config.cell_dim[0])
            col = int(x / game_config.cell_dim[1])
            pos = [float(x + float(game_config.cell_dim[1] / 2.0)),
                   float(y + float(game_config.cell_dim[0] / 2.0))]
            cell = CellSprite(pos, game_config.cell_dim,
                              game_state.window_grid.grid[row][col], game_config.color_mode)
            game_state.all_sprites.add(cell)
            # key = "x,y" and val = CellSprite object
            game_state.sprite_map[f'{x},{y}'] = cell


def dynamic_grid_sprite_update(game_config, game_state, cell_dim, window_dim):

    # game_grid = grid.initialize_grid_from_window_size(cell_dim, window_dim)

    # rows = len(game_grid)
    # cols = len(game_grid[0])
    window_grid = WindowGrid(cell_dim, window_dim)

    game_state.all_sprites.empty()

    # game_state = GameState2D(
    #     window_grid, 0, game_state.fps, game_state.display_surface, game_state.all_sprites, {})

    # game_config = GameConfig(cell_dim, window_dim, game_config.color_mode)

    game_state.update(window_grid, 0, game_state.fps,
                      game_state.display_surface, game_state.all_sprites, {})

    game_config.update(cell_dim, window_dim, game_config.color_mode)

    game_state.window_grid.randomize_grid()

    initiaize_grid_sprites(game_config, game_state)

    # return {"game_config": game_config, "game_state": game_state}


def reset_all_sprites_to_dead(game_state, game_config):

    game_state.window_grid.reinitialize_to_all_dead()

    for y in range(0, game_config.window_dim[1], game_config.cell_dim[1]):
        for x in range(0, game_config.window_dim[0], game_config.cell_dim[0]):
            row = int(y / game_config.cell_dim[0])
            col = int(x / game_config.cell_dim[1])

            sprite_key = f'{x},{y}'
            if sprite_key in game_state.sprite_map:
                cell_sprite = game_state.sprite_map[sprite_key]
                is_alive = game_state.window_grid.grid[row][col]
                cell_sprite.update_cell(
                    is_alive, game_config.color_mode)
