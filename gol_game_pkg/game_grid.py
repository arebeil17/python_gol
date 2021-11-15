from gol_game_pkg.game_constants import GRID_MOVES_DICT as grid_moves
import random


class GameGrid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = self.make_grid()

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
                adj_live_cells += self.grid[adj_row][adj_col]

        return adj_live_cells

    def copy_grid(self):
        grid_copy = [[0 for i in range(self.cols)] for j in range(self.rows)]
        for row in range(0, self.rows):
            for col in range(0, self.cols):
                grid_copy[row][col] = self.grid[row][col]
        return grid_copy

    def evaluate_grid(self):
        updated_grid = self.copy_grid()
        num_updates = 0
        for row in range(0, self.rows):
            for col in range(0, self.cols):

                num_adj_alive = self.compute_alive_adj_cells(row, col)

                if self.grid[row][col] == 1:
                    # Cell dies if under/over-population conditon is true
                    if num_adj_alive < 2 or num_adj_alive > 3:
                        updated_grid[row][col] = 0  # Death of cell
                        num_updates += 1
                elif self.grid[row][col] == 0 and num_adj_alive == 3:
                    updated_grid[row][col] = 1  # Reproduction
                    num_updates += 1

        self.grid = updated_grid

        return num_updates

    def randomize_grid(self):
        for row in self.grid:
            num_live = self.rows
            while num_live > 0:
                random_index = random.randint(0, len(row) - 1)
                row[random_index] = 1
                num_live -= 1


class WindowGrid(GameGrid):
    def __init__(self, cell_dim, window_dim):
        self.cell_dim = cell_dim
        self.window_dim = window_dim

        num_rows = int(window_dim[1] / cell_dim[1])
        num_cols = int(window_dim[0] / cell_dim[0])
        super().__init__(num_rows, num_cols)

    def initialize_from_cell_and_window_dim(self):

        self.rows = int(self.window_dim[1] / self.cell_dim[1])
        self.cols = int(self.window_dim[0] / self.cell_dim[0])

        self.grid = super().make_grid()
