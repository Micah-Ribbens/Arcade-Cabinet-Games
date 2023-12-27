from game_qu.gui_components.navigation_screen import NavigationScreen
from games.bird_shooter.bird_shooter_screen import BirdShooterScreen
from games.no_internet_game.no_internet_game_screen import NoInternetGameScreen
from games.space_shooter.space_shooter_screen import SpaceShooterScreen
from games.platformer.platformer_screen import PlatformerScreen
from game_qu.gui_components.screen import Screen
from game_qu.base.important_variables import *


class MainScreen(NavigationScreen):
    """The main screen of the application (allows the player to navigate to all the other games)"""

    screen_names = ["Bird Shooter", "No Internet Game", "Space Shooter", "Robowars"]
    screens = [BirdShooterScreen(), NoInternetGameScreen(), SpaceShooterScreen(), PlatformerScreen()]

    def __init__(self):
        """Initializes the game"""

        button_shortcuts = {
            BUTTON_SELECT: self.screens[1],
            BUTTON_START: self.screens[2]
        }
        key_shortcuts = {
            KEY_H: self.screens[0],
            KEY_J: self.screens[1],
            KEY_K: self.screens[2],
            KEY_L: self.screens[3]
        }

        game_button_shortcuts = button_shortcuts if IS_USING_CONTROLLER else key_shortcuts
        super().__init__(self.screen_names, self.screens, screen_shortcut_game_buttons=game_button_shortcuts)
