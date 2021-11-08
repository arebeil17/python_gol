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
from gol_game_pkg.game_constants import RGB_COLOR_DICT as rgb_dict
from gol_game_pkg.game_types import GameState2D, GameConfig
import colorama

HEIGHT = 600
WIDTH = 1000
ACC = 0.5
FRIC = -0.12
FPS = 30


def create_text_bar(window_dim, info_string):
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)

    font = pygame.font.Font('freesansbold.ttf', 20)

    text = font.render(info_string, True, white, None)

    textRect = text.get_rect()

    textRect.center = (window_dim[0] // 2, window_dim[1] - 20)

    return text, textRect


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


def cursor_mode_2d(game_config, game_state):

    exit_cursor_mode = False
    while not exit_cursor_mode:
        mouse_up_detected = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_up_detected = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                print("Exiting Cursor mode!")
                exit_cursor_mode = True
                continue

        for y in range(game_config.cell_dim[1], game_config.window_dim[1], game_config.cell_dim[1]):
            for x in range(game_config.cell_dim[0], game_config.window_dim[0], game_config.cell_dim[0]):
                row = int(y / game_config.cell_dim[0])
                col = int(x / game_config.cell_dim[1])
                pos = [x, y]

                sprite_key = f'{x},{y}'
                if sprite_key in game_state.sprite_map:
                    cell_sprite = game_state.sprite_map[sprite_key]
                    if mouse_up_detected and cell_sprite.is_clicked():
                        print("Detected clicked sprite at: ", x, ",", y)
                        game_state.game_grid[row][col] = not game_state.game_grid[row][col]

                    is_alive = game_state.game_grid[row][col]
                    cell_sprite.update_cell(
                        is_alive, game_config.color_mode)

        game_state.all_sprites.update()
        game_state.displaysurface.fill((0, 0, 0))

        for entity in game_state.all_sprites:
            game_state.displaysurface.blit(entity.surf, entity.rect)

        pygame.display.flip()

        pygame.time.Clock().tick(FPS)


def simualtion_mode_2d(game_config, game_state):

    simulation_paused = False
    generations = 0
    while True:
        info_string = f'Generation: {generations} Updates: {game_state.updates}'
        text, text_rect = create_text_bar(game_config.window_dim, info_string)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                print("Simulation toggled Enter key pressed!")
                simulation_paused = not simulation_paused

        if not simulation_paused:

            for y in range(game_config.cell_dim[1], HEIGHT, game_config.cell_dim[1]):
                for x in range(game_config.cell_dim[0], WIDTH, game_config.cell_dim[0]):
                    row = int(y / game_config.cell_dim[0])
                    col = int(x / game_config.cell_dim[1])

                    sprite_key = f'{x},{y}'
                    if sprite_key in game_state.sprite_map:
                        cell_sprite = game_state.sprite_map[sprite_key]
                        is_alive = game_state.game_grid[row][col]
                        cell_sprite.update_cell(
                            is_alive, game_config.color_mode)

            game_state.all_sprites.update()
            game_state.display_surface.fill((0, 0, 0))

            for entity in game_state.all_sprites:
                game_state.display_surface.blit(entity.surf, entity.rect)

            game_state.display_surface.blit(text, text_rect)

            game_state = grid.evaluate_grid(
                game_state, game_config.grid_dim[1], game_config.grid_dim[0])

            generations += 1

            pygame.display.flip()

        game_state.all_sprites.remove(text_rect)
        pygame.time.Clock().tick(FPS)
