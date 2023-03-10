from game_qu.base.important_variables import (
    SCREEN_HEIGHT,
    SCREEN_LENGTH,
)

from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.gui_components.component import Component
from game_dependencies.platformer.game_object import GameObject


class Platform(Component, GameObject):
    """The platform that the players can jump onto and interact with"""

    color = (150, 75, 0)
    object_type = "Platform"

    def __init__(self, top_edge=0, left_edge=0, length=0, height=0):
        """Initializes the object"""

        super().__init__("games/platformer/images/platform.png")
        self.number_set_dimensions(top_edge, left_edge, length, height)


