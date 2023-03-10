import os

from game_qu.base.important_variables import *
from game_qu.base.colors import light_gray
from game_qu.base.game_runner_function import run_game
from game_qu.gui_components.component import Component
from game_qu.gui_components.grid import Grid
from game_qu.gui_components.screen import Screen
from game_qu.gui_components.dimensions import Dimensions
from math import sqrt

screen = Screen()
screen.background_color = light_gray

file_paths = ""
file_path_start = "games/platformer/images"

for file_name in os.listdir(file_path_start):
    screen.components.append(Component(f"{file_path_start}/{file_name}"))

grid = Grid(Dimensions(0, 0, SCREEN_LENGTH, SCREEN_HEIGHT), int(sqrt(len(screen.components))), None)
grid.turn_into_grid(screen.components, None, None, False)
run_game(screen)