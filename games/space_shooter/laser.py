from game_qu.gui_components.component import Component
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.gui_components.dimensions import Dimensions
from game_qu.base.important_variables import *


class Laser(Component):
    """What the player's shoot to attack the meteorites"""

    velocity = VelocityCalculator.get_velocity(SCREEN_HEIGHT, 500)
    height = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 9)
    length = VelocityCalculator.get_dimension(SCREEN_LENGTH, 4)
    damage = 0

    def __init__(self, horizontal_midpoint, bottom_edge, path_to_image, size_multiplier, damage):
        """Initializes the laser with the provided attributes and location"""

        self.length = self.length * size_multiplier
        self.height = self.height * size_multiplier
        self.damage, self.path_to_image = damage, path_to_image

        top_edge = bottom_edge - self.height
        left_edge = horizontal_midpoint - self.length / 2
        super().__init__(path_to_image)

        Dimensions.__init__(self, left_edge, top_edge, self.length, self.height)

    def run(self):
        """Moves the laser upwards"""

        self.top_edge -= VelocityCalculator.get_distance(self.velocity)


