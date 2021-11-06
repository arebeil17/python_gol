import time
from math import floor
import gol_game_pkg.grid as grid
import gol_game_pkg.display as display
from gol_game_pkg.game_constants import GRID_MOVES_DICT as grid_moves
from gol_game_pkg.game_constants import USER_INPUT_TO_MOVE_DICT as input_to_move
from gol_game_pkg.game_types import GameState


def cursor_mode(game_grid, rows, cols, output_stream):

    cursor = [int(rows / 2), int(cols / 2)]  # cursor list [x, y]
    display.clear()
    print("Initial state of grid:")

    display.print_cursor(game_grid, rows, cols, cursor, output_stream)

    while(True):
        user_input = ""
        user_input = input(
            "Enter A,W,S,D to move, just enter to toggle cell or Q to quit(): ")

        user_input = user_input.lower()

        if user_input == "q":
            break

        move = [0, 0]
        if user_input in input_to_move:

            move = grid_moves[input_to_move[user_input]]

            if not grid.boundary_check(rows, cols, cursor[0] + move[0], cursor[1] + move[1]):
                print("Move out of bounds!")
                continue

        elif user_input == "":
            game_grid[cursor[0]][cursor[1]] ^= 1  # xor to toggle cell
        elif user_input == "q":
            print("Exiting cursor mode.")
            break
        else:
            print("Invalid input. Please try again.")
            continue

        cursor = [cursor[0] + move[0], cursor[1] + move[1]]

        display.print_cursor(game_grid, rows, cols, cursor, output_stream)

    return game_grid


def simulate_mode(game_grid, rows, cols, auto, color_mode, output_stream):

    generations = 0
    prev_cell_updates = 0

    display.clear()
    print("Initial state of grid:")

    state = GameState(game_grid, 0)

    if color_mode == "1":
        display.print_grid(state.game_grid, output_stream,
                           generations, state.updates)
    elif color_mode == "2":
        display.print_disco_grid(state.game_grid, output_stream,
                                 generations, state.updates)

    update_delta = 0
    stale_delta = 0

    while(True):
        if auto == 'y':
            time.sleep(0.25)
        else:
            user_input = input("Hit Enter to continue or Q to quit(): ")
            if user_input.lower() == "q":
                break

        state = grid.evaluate_grid(state, rows, cols)

        generations += 1

        if color_mode == "1":
            display.print_grid(state.game_grid, output_stream,
                               generations, state.updates)
        elif color_mode == "2":
            display.print_disco_grid(state.game_grid, output_stream,
                                     generations, state.updates)

        if prev_cell_updates == state.updates:
            print("\nGrowth has ended at generation:", generations,
                  "Total updates:", state.updates)
            print("Simulation ended!")
            break
        else:
            if update_delta == state.updates - prev_cell_updates:
                stale_delta += 1
            else:
                stale_delta = 0
            update_delta = state.updates - prev_cell_updates

        if stale_delta == 10:
            print("Board has reached steady state. Exiting infinite generation state.")
            print("\nGrowth has ended at generation:", generations - stale_delta,
                  "Total updates:", state.updates)
            print("Simulation ended!")
            break

        prev_cell_updates = state.updates
