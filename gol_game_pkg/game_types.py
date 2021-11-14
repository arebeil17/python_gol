import pygame


class GameState:
    def __init__(self, game_grid, updates):
        self.game_grid = game_grid
        self.updates = updates


class GameState2D(GameState):
    def __init__(self, game_grid, updates, fps, display_surface, all_sprites, sprite_map):
        super().__init__(game_grid, updates)
        self.fps = fps
        self.display_surface = display_surface
        self.all_sprites = all_sprites
        self.sprite_map = sprite_map


class GameConfig:
    def __init__(self, cell_dim, grid_dim, window_dim, color_mode):
        self.cell_dim = cell_dim
        self.grid_dim = grid_dim
        self.window_dim = window_dim
        self.color_mode = color_mode
