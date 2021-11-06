from colorama import Fore, Back, Style
import sys
import random
from os import system, name
import gol_game_pkg.game_constants as game_constants


def title_screen():

    print("\n" + Fore.GREEN + "■ ■ ■ ■    ■ ■      ■   ■    ■ ■ ■ ■")
    print(Fore.RED + "■        ■     ■  ■   ■   ■  ■      ")
    print(Fore.CYAN + "■   ■ ■  ■ ■ ■ ■  ■   ■   ■  ■ ■ ■ ■")
    print(Fore.YELLOW + "■     ■  ■     ■  ■   ■   ■  ■      ")
    print(Fore.MAGENTA + "■ ■ ■ ■  ■     ■  ■   ■   ■  ■ ■ ■ ■\n")

    print(Fore.BLUE + "■ ■ ■ ■  ■ ■ ■ ■     ■         ■  ■ ■ ■ ■  ■ ■ ■ ■")
    print(Fore.CYAN + "■     ■  ■           ■         ■  ■        ■      ")
    print(Fore.GREEN + "■     ■  ■ ■ ■ ■     ■         ■  ■ ■ ■ ■  ■ ■ ■ ■")
    print(Fore.MAGENTA + "■     ■  ■           ■         ■  ■        ■      ")
    print(Fore.YELLOW +
          "■ ■ ■ ■  ■           ■ ■ ■ ■   ■  ■        ■ ■ ■ ■" + Style.RESET_ALL + "\n")


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

        if row[0] == 1:
            gen_row_string += Fore.GREEN
        else:
            gen_row_string += Fore.RED
        prev_cell = row[0]

        for cell in row:
            if cell == 1:
                if cell == prev_cell:
                    gen_row_string += chr(0x25A0)
                else:
                    gen_row_string += Fore.GREEN + chr(0x25A0)
            else:
                if cell == prev_cell:
                    gen_row_string += chr(0x25A1)
                else:
                    gen_row_string += Fore.RED + chr(0x25A1)

            gen_row_string += " "

            prev_cell = cell

        gen_grid_string += gen_row_string

    output_string = gen_grid_string + Style.RESET_ALL + \
        " \nGeneration: " + str(generations) + \
        " Cell updates: " + str(total_cell_updates) + "\n"
    clear()
    output_stream.write(output_string)
    output_stream.flush()


def print_disco_grid(grid, output_stream, generations, total_cell_updates):

    gen_grid_string = ""
    for row in grid:
        gen_row_string = "\n"

        for cell in row:
            if cell == 1:
                rand_color = random.choice(game_constants.DISCO_MODE_LIST)
                gen_row_string += rand_color + chr(0x25A0)
            else:
                gen_row_string += " "

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
