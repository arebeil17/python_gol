from colorama import Fore, Back, Style

GRID_MOVES_DICT = {"left": (0, -1), "right": (0, 1),
                   "down": (1, 0), "up": (-1, 0),
                   "up_left": (-1, -1), "up_right": (-1, 1),
                   "down_left": (1, -1), "down_right": (1, 1)}

USER_INPUT_TO_MOVE_DICT = {"a": "left", "d": "right", "w": "up", "s": "down"}

DISCO_MODE_LIST = [Fore.RED, Fore.YELLOW,
                   Fore.CYAN, Fore.GREEN, Fore.MAGENTA, Fore.BLUE]
