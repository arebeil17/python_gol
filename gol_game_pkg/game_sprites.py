import pygame
from pygame import Color, Surface
import random
from gol_game_pkg.game_constants import RGB_COLOR_DICT as rgb_dict


class CellSprite(pygame.sprite.Sprite):
    def __init__(self,  pos, cell_dim, is_alive, disco):
        super().__init__()
        self.surf = pygame.Surface((cell_dim[0], cell_dim[1]))
        if is_alive:
            if disco:
                random_color = random.choice(list(rgb_dict.values()))
                self.surf.fill(random_color)
            else:
                self.surf.fill((128, 255, 40))  # RGB - GREEN
        else:
            self.surf.fill((10, 10, 10))
        # self.surf.fill((202, 0, 52))  # RGB - RED
        self.rect = self.surf.get_rect(center=(pos[0], pos[1]))

    def update_cell(self, is_alive, disco):
        if is_alive:
            if disco:
                random_color = random.choice(list(rgb_dict.values()))
                self.surf.fill(random_color)
            else:
                self.surf.fill((128, 255, 40))  # RGB - GREEN
        else:
            self.surf.fill((10, 10, 10))

    def is_clicked(self):
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())


def initiaize_grid_sprites(game_config, game_state):
    for y in range(game_config.cell_dim[1], game_config.window_dim[1], game_config.cell_dim[1]):
        for x in range(game_config.cell_dim[0], game_config.window_dim[0], game_config.cell_dim[0]):
            row = int(y / game_config.cell_dim[0])
            col = int(x / game_config.cell_dim[1])
            pos = [x, y]
            cell = CellSprite(pos, game_config.cell_dim,
                              game_state.game_grid[row][col], game_config.color_mode)
            game_state.all_sprites.add(cell)
            # key = "x,y" and val = CellSprite object
            game_state.sprite_map[f'{x},{y}'] = cell
