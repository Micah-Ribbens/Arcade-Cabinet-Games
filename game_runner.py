"""The main file that runs the game"""

from game_qu.base.library_changer import LibraryChanger

# IMPORTANT: This has to here, so the library things can be set
LibraryChanger.set_game_library("pygame")
# LibraryChanger.set_full_screen(True)
LibraryChanger.set_screen_dimensions(1000, 600)
LibraryChanger.set_important_constant("IS_USING_CONTROLLER", False)

from game_qu.base.game_runner_function import run_game
from main_screen import MainScreen

if __name__ == "__main__":
    run_game(MainScreen())