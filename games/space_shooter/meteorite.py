from game_qu.gui_components.dimensions import Dimensions
from game_qu.base.lines import LineSegment, Point
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.gui_components.component import Component
from game_qu.base.important_variables import *


class Meteorite(Component):
    length = VelocityCalculator.get_dimension(SCREEN_LENGTH, 8)
    height = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 17)
    left_edge_path = None
    top_edge_path = None
    time_on_path = 0
    hit_points = 4
    last_player_hit_by = 0

    def __init__(self, meteorite_path, time_for_completion):
        super().__init__("games/space_shooter/images/meteorite.png")
        Dimensions.__init__(self, 0, 0, self.length, self.height)

        self.left_edge_path = LineSegment(Point(0, meteorite_path.start_point.x_coordinate),
                                          Point(time_for_completion, meteorite_path.end_point.x_coordinate))

        self.top_edge_path = LineSegment(Point(0, meteorite_path.start_point.y_coordinate),
                                          Point(time_for_completion, meteorite_path.end_point.y_coordinate))

    def run(self):
        self.time_on_path += VelocityCalculator.time

        self.left_edge = self.left_edge_path.get_y_coordinate(self.time_on_path)
        self.top_edge = self.top_edge_path.get_y_coordinate(self.time_on_path)