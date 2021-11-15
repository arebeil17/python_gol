import random
from colorama import Fore, Back, Style
from gol_game_pkg.game_constants import GRID_MOVES_DICT as grid_moves
from gol_game_pkg.game_types import GameState


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.game_grid = self.make_grid(rows, cols)

    def make_grid(self):
        return [[0 for i in range(self.cols)] for j in range(self.rows)]

    def boundary_check(self, row, col):
        return (row in range(0, self.rows) and col in range(0, self.cols))

    def compute_alive_adj_cells(self, current_row, current_col):
        adj_live_cells = 0
        for move in grid_moves.values():

            adj_row = current_row + move[0]
            adj_col = current_col + move[1]

            if self.boundary_check(adj_row, adj_col):
                adj_live_cells += self.game_grid[adj_row][adj_col]

        return adj_live_cells

    def copy_grid(self):
        grid_copy = [[0 for i in range(self.cols)] for j in range(self.rows)]
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                grid_copy[row][col] = self.game_grid[row][col]
        return grid_copy

    def evaluate_grid(self):
        updated_grid = self.copy_grid()
        num_updates = 0
        for row in range(0, self.rows):
            for col in range(0, self.cols):

                num_adj_alive = self.compute_alive_adj_cells(row, col)

                if self.game_grid[row][col] == 1:
                    # Cell dies if under/over-population conditon is true
                    if num_adj_alive < 2 or num_adj_alive > 3:
                        updated_grid[row][col] = 0  # Death of cell
                        num_updates += 1
                elif self.game_grid[row][col] == 0 and num_adj_alive == 3:
                    updated_grid[row][col] = 1  # Reproduction
                    num_updates += 1

        self.game_grid = updated_grid

        return num_updates


class Grid(Grid):
    def __init__(self, cell_dim, window_dim):
        self.cell_dim = cell_dim
        self.window_dim = window_dim

        num_rows = int(window_dim[1] / cell_dim[1])
        num_cols = int(window_dim[0] / cell_dim[0])
        super().__init__(num_rows, num_cols)

    def initialize_from_cell_and_window_dim(self):

        self.rows = int(self.window_dim[1] / self.cell_dim[1])
        self.cols = int(self.window_dim[0] / self.cell_dim[0])

        self.game_grid = self.make_grid(self.rows, self.cols)


def boundary_check(rows, cols, row, col):
    return (row in range(0, rows) and col in range(0, cols))


def initialize_grid_from_window_size(cell_dim, window_dim):

    rows = int(window_dim[1] / cell_dim[1])
    cols = int(window_dim[0] / cell_dim[0])

    game_grid = make_grid(rows, cols)

    return game_grid


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
    num_updates = 0
    for row in range(0, rows):
        for col in range(0, cols):
            num_adj_alive = compute_alive_adj_cells(
                rows, cols, row, col, state.game_grid)

            if state.game_grid[row][col] == 1:
                # Cell dies if under/over-population conditon is true
                if num_adj_alive < 2 or num_adj_alive > 3:
                    updated_grid[row][col] = 0  # Death of cell
                    num_updates += 1
            elif state.game_grid[row][col] == 0 and num_adj_alive == 3:
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
