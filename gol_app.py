import pygame
import gol_game_pkg.game_control as game_control
from gol_game_pkg.game_constants import GameMode
from pygame.locals import *
import gol_game_pkg.game_sprites as game_sprites
from gol_game_pkg.game_gui import GameGui

game_init_list = game_control.initialize_game()
game_state = game_init_list[0]
game_config = game_init_list[1]

game_gui = GameGui(game_config)

game_control.run_main_menu(game_gui, game_state, game_config)

if GameMode(game_config.get_current_selection("mode")[1]) == GameMode.Cursor:
    game_sprites.reset_all_sprites_to_dead(game_state, game_config)
    game_control.cursor_mode_2d(game_config, game_state)

game_control.simualtion_mode_2d(game_gui, game_config, game_state)
