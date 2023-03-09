from base.library_changer import LibraryChanger
import cProfile

LibraryChanger.set_screen_dimensions(1050, 800)
LibraryChanger.set_game_library("pygame")

from base.game_runner_function import run_game
from main_screen import MainScreen


# Have to use try except because pygame throws an error when the application is closed
# cProfile.run("run_game(MainScreen())", None, "tottime")
run_game(MainScreen())