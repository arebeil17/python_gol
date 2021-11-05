import random
import time
from colorama import Fore, Back, Style
from os import system, name
import sys
from game_constants import GRID_MOVES_DICT as grid_moves
import game_modes
from game_types import GameState


def boundary_check(rows, cols, row, col):
    return (row in range(0, rows) and col in range(0, cols))


def compute_alive_adj_cells(rows, cols, current_row, current_col, grid):
    adj_live_cells = 0
    for move in grid_moves.values():

        adj_row = current_row + move[0]
        adj_col = current_col + move[1]

        if boundary_check(rows, cols, adj_row, adj_col):
            adj_live_cells += grid[adj_row][adj_col]

    return adj_live_cells


def evaluate_grid(state, rows, cols):
    updated_grid = copy_grid(state.game_grid, rows, cols)
    DEAD = 0
    ALIVE = 1
    num_updates = 0
    for row in range(0, rows):
        for col in range(0, cols):
            num_adj_alive = compute_alive_adj_cells(
                rows, cols, row, col, state.game_grid)

            if state.game_grid[row][col] == ALIVE:
                # Cell dies if under/over-population conditon is true
                if num_adj_alive < 2 or num_adj_alive > 3:
                    updated_grid[row][col] = 0  # Death of cell
                    num_updates += 1
            elif state.game_grid[row][col] == DEAD and num_adj_alive == 3:
                updated_grid[row][col] = 1  # Reproduction
                num_updates += 1

    state.game_grid = updated_grid
    state.updates += num_updates

    return state


def make_grid(rows, cols):
    return [[0 for i in range(cols)] for j in range(rows)]


def copy_grid(grid, rows, cols):
    grid_copy = [[0 for i in range(cols)] for j in range(rows)]
    for row in range(0, rows):
        for col in range(0, cols):
            grid_copy[row][col] = grid[row][col]
    return grid_copy


def randomize_grid(grid, num_live_per_row):
    for row in grid:
        num_live = num_live_per_row
        while num_live > 0:
            random_index = random.randint(0, len(row) - 1)
            row[random_index] = 1
            num_live -= 1
    return grid


def blinker_grid(grid, rows):

    mid_row = rows / 2
    row_cnt = 0
    for row in grid:
        cell_index = 0
        for cell_index in range(0, len(row)):
            if mid_row == row_cnt and cell_index % 4 != 0:
                row[cell_index] = 1
            cell_index += 1

        row_cnt += 1

    return grid


def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def print_grid(grid, output_stream, generations, total_cell_updates):

    gen_grid_string = ""
    for row in grid:
        gen_row_string = "\n"
        for cell in row:
            if cell == 1:
                gen_row_string += Fore.GREEN + chr(0x25A0)
            else:
                gen_row_string += Fore.RED + chr(0x25A1)
            gen_row_string += " "

        gen_grid_string += gen_row_string

    output_string = gen_grid_string + Style.RESET_ALL + \
        " \nGeneration: " + str(generations) + \
        " Cell updates: " + str(total_cell_updates) + "\n"
    clear()
    output_stream.write(output_string)
    output_stream.flush()


def print_cursor(grid, rows, cols, cursor, output_stream):

    gen_grid_string = ""
    for row in range(0, rows):
        gen_row_string = "\n"
        for col in range(0, cols):

            if row == cursor[0] and col == cursor[1]:
                gen_row_string += Fore.MAGENTA + chr(0x25A0)
            elif grid[row][col] == 1:
                gen_row_string += Fore.GREEN + chr(0x25A0)
            else:
                gen_row_string += Fore.RED + chr(0x25A1)
            gen_row_string += " "

        gen_grid_string += gen_row_string

    clear()
    output_string = gen_grid_string + Style.RESET_ALL + "\n"
    output_stream.write(output_string)
    output_stream.flush()
