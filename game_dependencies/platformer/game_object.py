from game_qu.base.important_variables import (
    SCREEN_HEIGHT,
    SCREEN_LENGTH,
)

from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.gui_components.component import Component


class GameObject:
    """A class that use is for providing functions and attributes that must be in common for all game objects (or at least almost all)"""

    object_type = ""

    def update_for_side_scrolling(self, amount):
        """Updates the inanimate object, so it side scrolls"""

        self.left_edge -= amount

