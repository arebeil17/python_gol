import time
import sys
import random
import game_modes
import grid

rows = int(input("Specify number of rows: "))
cols = int(input("Specify number of cols: "))

auto = ""
while True:
    auto = input("Would you like game to automatically generate (Y/N): ")
    auto = auto.lower()
    if auto == "y" or auto == "n":
        break

mode_selected = ""
print("""\nPlease select game grid setup:
1) Cursor mode: Manual set the board
2) Random mode: Randomly generate the board
""")
while True:
    mode_selected = input("Enter selection: ")
    if mode_selected == "1" or mode_selected == "2":
        print("Selected board initialization mode:", mode_selected)
        break
    else:
        print("Invalid board initialization mode selected.")
        continue

game_grid = grid.make_grid(rows, cols)

output_stream = sys.stdout

if mode_selected == "1":
    game_grid = game_modes.cursor_mode(game_grid, rows, cols, output_stream)
else:
    game_grid = grid.randomize_grid(game_grid, rows)

game_modes.simulate_mode(game_grid, rows, cols, auto, output_stream)
