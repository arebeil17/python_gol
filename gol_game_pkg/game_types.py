import pygame
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


class GameConfig:
    def __init__(self, cell_dim, window_dim, color_mode):
        self.cell_dim = cell_dim
        self.window_dim = window_dim
        self.color_mode = color_mode
