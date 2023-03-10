from game_qu.base.library_changer import LibraryChanger

# IMPORTANT: This has to here, so the library things can be set
LibraryChanger.set_screen_dimensions(2200, 1300)
LibraryChanger.set_important_constant("IS_USING_CONTROLLER", False)
LibraryChanger.set_game_library("pygame")

from game_qu.base.game_runner_function import run_game
from main_screen import MainScreen

run_game(MainScreen())