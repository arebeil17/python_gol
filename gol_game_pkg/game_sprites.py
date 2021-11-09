import pygame
from pygame import Color, Surface
import random
from gol_game_pkg.game_constants import RGB_COLOR_DICT as rgb_dict
from gol_game_pkg.game_constants import CellColor


class CellSprite(pygame.sprite.Sprite):
    def __init__(self,  pos, cell_dim, is_alive, color_mode):
        super().__init__()
        self.surf = pygame.Surface((cell_dim[0], cell_dim[1]))
        self.random_color = random.choice(list(rgb_dict.values()))
        if is_alive:
            if CellColor(color_mode) == CellColor.Disco or CellColor(color_mode) == CellColor.Colorful:
                self.surf.fill(self.random_color)
            else:
                self.surf.fill((128, 255, 40))  # RGB - GREEN
        else:
            self.surf.fill((10, 10, 10))

        self.rect = self.surf.get_rect(center=(pos[0], pos[1]))

    def update_cell(self, is_alive, color_mode):
        if is_alive:
            if CellColor(color_mode) == CellColor.Disco:
                random_color = random.choice(list(rgb_dict.values()))
                self.surf.fill(random_color)
            elif CellColor(color_mode) == CellColor.Colorful:
                self.surf.fill(self.random_color)
            else:
                self.surf.fill((128, 255, 40))  # RGB - GREEN
        else:
            self.surf.fill((10, 10, 10))

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())


def initiaize_grid_sprites(game_config, game_state):
    for y in range(0, game_config.window_dim[1], game_config.cell_dim[1]):
        for x in range(0, game_config.window_dim[0], game_config.cell_dim[0]):
            row = int(y / game_config.cell_dim[0])
            col = int(x / game_config.cell_dim[1])
            pos = [float(x + float(game_config.cell_dim[1] / 2.0)),
                   float(y + float(game_config.cell_dim[0] / 2.0))]
            cell = CellSprite(pos, game_config.cell_dim,
                              game_state.game_grid[row][col], game_config.color_mode)
            game_state.all_sprites.add(cell)
            # key = "x,y" and val = CellSprite object
            game_state.sprite_map[f'{x},{y}'] = cell
