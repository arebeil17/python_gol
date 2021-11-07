import time
import sys
import random
import gol_game_pkg.game_modes as game_modes
import gol_game_pkg.grid as grid
import gol_game_pkg.display as display
import colorama

colorama.init()

display.title_screen()
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
4) Exit
""")

while True:
    mode_selected = input("Enter selection: ")
    if mode_selected == "1" or mode_selected == "2":
        print("Selected board initialization mode:", mode_selected)
        break
    elif mode_selected == "4":
        print("Exiting game. Goodbye!")
        sys.exit(0)
    else:
        print("Invalid board initialization mode selected.")
        continue

print("Select display colors for live cells: ")
print("1) Default")
print("2) Disco/Random")
print("3) Exit")
while True:
    color_mode = input("Enter selection: ")

    if color_mode == "1" or color_mode == "2":
        break
    elif color_mode == "3":
        print("Exiting game. Goodbye!")
        sys.exit(0)
    else:
        print("Please enter valid choice.")


game_grid = grid.make_grid(rows, cols)

output_stream = sys.stdout

if mode_selected == "1":
    game_grid = game_modes.cursor_mode(game_grid, rows, cols, output_stream)
else:
    game_grid = grid.randomize_grid(game_grid, rows)

game_modes.simulate_mode(game_grid, rows, cols, auto,
                         color_mode, output_stream)
