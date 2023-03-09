import os

from base.important_variables import *
from base.colors import light_gray
from base.game_runner_function import run_game
from gui_components.component import Component
from gui_components.grid import Grid
from gui_components.screen import Screen
from gui_components.dimensions import Dimensions
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