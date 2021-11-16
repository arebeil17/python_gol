from colorama import Fore, Back, Style
import enum
GRID_MOVES_DICT = {"left": (0, -1), "right": (0, 1),
                   "down": (1, 0), "up": (-1, 0),
                   "up_left": (-1, -1), "up_right": (-1, 1),
                   "down_left": (1, -1), "down_right": (1, 1)}

USER_INPUT_TO_MOVE_DICT = {"a": "left", "d": "right", "w": "up", "s": "down"}

DISCO_MODE_LIST = [Fore.RED, Fore.YELLOW,
                   Fore.CYAN, Fore.GREEN, Fore.MAGENTA, Fore.BLUE]

CELL_COLORS = {"ORANGE": (245, 100, 32),
               "PURPLE": (113, 103, 206),
               "BLUE": (56, 169, 240),
               "GREEN": (21, 197, 52),
               "LIME": (200, 234, 83),
               "YELLOW": (233, 220, 9),
               "RED": (245, 30, 60)}

GAME_COLORS = {"ORANGE": (245, 100, 32),
               "PURPLE": (113, 103, 206),
               "BLUE": (56, 169, 240),
               "GREEN": (21, 197, 52),
               "MATRIX_GREEN": (128, 255, 40),
               "LIME": (200, 234, 83),
               "YELLOW": (233, 220, 9),
               "RED": (245, 30, 60),
               "BLACK": (0, 0, 0),
               "GRAY": (20, 20, 35),
               "WHITE": (255, 255, 255)}


class CellColor(enum.Enum):
    Default = 0
    Colorful = 1
    Disco = 2


class GameMode(enum.Enum):
    Random = 0
    Cursor = 1
