import gol_game_pkg.game_control as game_control
from gol_game_pkg.game_constants import InitMode, CellColor
import pygame
from pygame import Color, Surface
from pygame.locals import *
import time
import sys
import random
import gol_game_pkg.grid as grid
import gol_game_pkg.game_sprites as game_sprites
from gol_game_pkg.game_types import GameConfig, GameState2D

cell_dim = [10, 10]
window_dim = [1000, 600]
board_init_mode = InitMode.Random
cell_color_mode = CellColor.Disco
FPS = 5


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

game_config = GameConfig(cell_dim, grid_dim, window_dim, cell_color_mode)

game_state = GameState2D(
    game_grid, 0, FPS, display_surface, all_sprites, sprite_map)


game_sprites.initiaize_grid_sprites(game_config, game_state)


if board_init_mode == InitMode.Random:
    game_state.game_grid = grid.randomize_grid(game_state.game_grid, rows)
else:
    game_control.cursor_mode_2d(game_config, game_state)

game_control.simualtion_mode_2d(game_config, game_state)
