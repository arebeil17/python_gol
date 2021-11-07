from gol_game_pkg.game_types import GameState
import pygame
from pygame import Color, Surface
from pygame.locals import *
import time
import sys
import random
import gol_game_pkg.game_modes as game_modes
import gol_game_pkg.grid as grid
import gol_game_pkg.display as display
import colorama

HEIGHT = 600
WIDTH = 800
ACC = 0.5
FRIC = -0.12
FPS = 10


class CellSprite(pygame.sprite.Sprite):
    def __init__(self,  pos, cell_dim, is_alive):
        super().__init__()
        self.surf = pygame.Surface((cell_dim[0], cell_dim[1]))
        if is_alive:
            self.surf.fill((128, 255, 40))  # RGB - GREEN
        else:
            self.surf.fill((10, 10, 10))
        # self.surf.fill((202, 0, 52))  # RGB - RED
        self.rect = self.surf.get_rect(center=(pos[0], pos[1]))


# class platform(pygame.sprite.Sprite):
#     def __init__(self):
#         super().__init__()
#         self.surf = pygame.Surface((WIDTH, 20))
#         self.surf.fill((255, 0, 0))
#         self.rect = self.surf.get_rect(center=(WIDTH/2, HEIGHT - 10))


pygame.init()
vec = pygame.math.Vector2  # 2 for two dimensional


FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


cell_dim = [10, 10]

rows = int(HEIGHT / cell_dim[1])
cols = int(WIDTH / cell_dim[0])

game_grid = grid.make_grid(rows, cols)

game_grid = grid.randomize_grid(game_grid, rows)

state = GameState(game_grid, 0)

empty = Color(0, 0, 0, 0)

all_sprites = pygame.sprite.Group()

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    for y in range(cell_dim[1], HEIGHT, cell_dim[1]):
        for x in range(cell_dim[0], WIDTH, cell_dim[0]):
            row = int(y / cell_dim[0])
            col = int(x / cell_dim[1])
            pos = [x, y]
            cell = CellSprite(pos, cell_dim, state.game_grid[row][col])
            all_sprites.add(cell)

    all_sprites.update()
    displaysurface.fill((0, 0, 0))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)

    state = grid.evaluate_grid(state, rows, cols)

    pygame.display.flip()

    all_sprites.empty()
    FramePerSec.tick(FPS)
