import random
import time
from colorama import Fore, Back, Style
from os import system, name
import sys

grid_moves = {"left": (0, -1), "right": (0, 1),
              "down": (-1, 0), "up": (1, 0),
              "diag_up_left": (1, -1), "diag_up_right": (1, 1),
              "diag_dwn_left": (-1, -1), "diag_dwn_right": (-1, 1)}


def boundary_check(rows, cols, adj_row, adj_col):
    if adj_row in range(rows) and adj_col in range(cols):
        return True
    return False


def compute_alive_adj_cells(rows, cols, current_row, current_col, grid):
    adj_live_cells = 0
    for move in grid_moves.values():

        adj_row = current_row + move[0]
        adj_col = current_col + move[1]

        if boundary_check(rows, cols, adj_row, adj_col):
            adj_live_cells += grid[adj_row][adj_col]

    return adj_live_cells


def evaluate_grid(grid, rows, cols):
    updated_grid = grid
    DEAD = 0
    ALIVE = 1
    num_updates = 0
    for row in range(0, rows):
        for col in range(0, cols):
            num_adj_alive = compute_alive_adj_cells(rows, cols, row, col, grid)

            if grid[row][col] == ALIVE:
                # Cell dies if under/over-population conditon is true
                if num_adj_alive < 2 or num_adj_alive > 3:
                    updated_grid[row][col] = DEAD
                    num_updates += 1
            elif grid[row][col] == DEAD and num_adj_alive == 3:
                updated_grid[row][col] = ALIVE  # Reproduction
                num_updates += 1

    return updated_grid, num_updates


def make_grid(rows, cols):
    return [[0 for i in range(cols)] for j in range(rows)]


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


def print_grid(grid):
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

    print(gen_grid_string, Style.RESET_ALL, end="")


rows = int(input("Specify number of rows: "))
cols = int(input("Specify number of cols: "))
auto = ""
while True:
    auto = input("Would you like game to automatically generate (Y/N): ")
    auto = auto.lower()
    if auto == "y" or auto == "n":
        break


grid = make_grid(rows, cols)
grid = randomize_grid(grid, rows)
#grid = blinker_grid(grid, rows)

generations = 0
num_cell_updates = 0
total_cell_updates = 0

clear()
print("Initial state of grid:")
print_grid(grid)

stale_cnt = 0

while(True):
    sys.stdout.flush()
    print("\nGeneration:", generations, "Cell updates:", total_cell_updates)

    if auto == 'y':

        time.sleep(0.10)
    else:
        user_input = input("Hit Enter to continue or Q to quit(): ")
        if user_input.lower() == "q":
            break

    clear()
    print_grid(grid)
    sys.stdout.flush()

    prev_cell_updates = num_cell_updates
    grid, num_cell_updates = evaluate_grid(grid, rows, cols)

    if prev_cell_updates == num_cell_updates:
        stale_cnt += 1
    else:
        stale_cnt = 0

    if stale_cnt == 2:
        print("\nGrowth has ended at generation:", generations,
              "Total updates:", total_cell_updates)
        print("Simulation ended!")
        break

    total_cell_updates += num_cell_updates
    generations += 1
