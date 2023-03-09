
from base.events import TimedEvent
from base.important_variables import *
from base.velocity_calculator import VelocityCalculator
from gui_components.component import Component
from gui_components.dimensions import Dimensions
from base.utility_functions import *
from games.space_shooter.laser import Laser
from base.important_variables import KEY_F


class Player(Component):
    path_to_laser_image = ""
    path_to_player_image = ""
    length = VelocityCalculator.get_dimension(SCREEN_LENGTH, 15)
    height = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 20)
    velocity = VelocityCalculator.get_velocity(SCREEN_LENGTH, 700)
    right_key = None
    left_key = None
    shoot_key = None
    lasers = []
    wait_to_shoot_event = None

    def __init__(self, left_key, right_key, shoot_key, path_to_player_image, path_to_laser_image):
        super().__init__(path_to_player_image)
        self.left_key, self.right_key, self.shoot_key = left_key, right_key, shoot_key
        self.path_to_laser_image = path_to_laser_image
        Dimensions.__init__(self, SCREEN_LENGTH / 2, SCREEN_HEIGHT - self.height, self.length, self.height)
        self.lasers = []
        self.wait_to_shoot_event = TimedEvent(.2)

    def run(self):
        self.movement()
        self.wait_to_shoot_event.run(self.wait_to_shoot_event.current_time >= self.wait_to_shoot_event.time_needed, False)

        if key_has_been_released(self.shoot_key) and self.wait_to_shoot_event.has_finished():
            self.shoot_laser(get_time_of_key_being_held_in(self.shoot_key))
            self.wait_to_shoot_event.start()

    def movement(self):
        distance = VelocityCalculator.get_distance(self.velocity)

        self.left_edge += distance if key_is_pressed(self.right_key) else 0
        self.left_edge -= distance if key_is_pressed(self.left_key) else 0

        self.left_edge = 0 if self.left_edge < 0 else self.left_edge
        self.left_edge = SCREEN_LENGTH - self.length if self.right_edge > SCREEN_LENGTH else self.left_edge

    def shoot_laser(self, time_held_in):
        size_multipliers = [1, 1.5, 2]
        times_needed_for_size_change = [.5, 1, float("inf")]

        size_multiplier_index = get_index_of_range(time_held_in, times_needed_for_size_change)
        size_multiplier = size_multipliers[size_multiplier_index]

        damage = size_multiplier_index + 1

        self.lasers.append(Laser(self.horizontal_midpoint, self.top_edge, self.path_to_laser_image, size_multiplier, damage))

    def reset(self):
        self.lasers = []
        self.wait_to_shoot_event.reset()

    def get_components(self):
        return self.lasers + [self]
