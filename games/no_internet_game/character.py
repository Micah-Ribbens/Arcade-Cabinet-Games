from game_qu.gui_components.dimensions import Dimensions
from game_qu.base.events import TimedEvent
from game_qu.base.important_variables import *
from game_qu.base.utility_functions import game_button_is_pressed, game_button_is_clicked
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.gui_components.component import Component
from game_qu.base.utility_functions import load_image


class Player(Component):
    length = VelocityCalculator.get_dimension(SCREEN_LENGTH, 13)
    height = VelocityCalculator.get_dimension(SCREEN_HEIGHT, 25)
    time_in_air = 0
    is_in_air = False
    jump_game_button = None
    right_game_button = None
    left_game_button = None
    forwards_velocity = VelocityCalculator.get_velocity(SCREEN_LENGTH, 500)
    animation_frame = 0
    base_path = "games/no_internet_game/images/Character6.0_000"
    next_frame_event = None
    max_right_edge = SCREEN_LENGTH
    game_is_paused = False
    total_frames = 2
    jump_frame = 2

    # Jumping
    gravity = 0
    upwards_velocity = 0
    initial_distance = 0
    vertex_height = 0

    def __init__(self, keys, ground_top_edge):
        self.left_game_button, self.right_game_button, self.jump_game_button = keys

        for x in range(self.total_frames):
            load_image(f"{self.base_path}{x}.png")

        super().__init__(f"{self.base_path}0.png")
        load_image(f"{self.base_path}{self.jump_frame}.png")
        self.initial_distance = ground_top_edge - self.height

        time_to_vertex = .4
        self.vertex_height = 270
        vertex = self.initial_distance - self.vertex_height

        # Gotten using math
        self.upwards_velocity = (-2 * self.initial_distance + 2 * vertex)/time_to_vertex
        self.gravity = 2*(self.initial_distance - vertex)/pow(time_to_vertex, 2)
        self.next_frame_event = TimedEvent(.1)

        self.number_set_dimensions(0, self.initial_distance, self.length, self.height)

    def run(self):
        if not self.game_is_paused:
            self.run_movement()
            self.run_animation()

    def run_movement(self):
        self.run_jumping()

        distance = VelocityCalculator.get_distance(self.forwards_velocity)

        self.left_edge += distance if game_button_is_pressed(self.right_game_button) else 0
        self.left_edge -= distance * 1.5 if game_button_is_pressed(self.left_game_button) else 0

        self.left_edge = 0 if self.left_edge < 0 else self.left_edge
        self.left_edge = self.max_right_edge - self.length if self.right_edge > self.max_right_edge else self.left_edge

    def run_jumping(self):
        if game_button_is_clicked(self.jump_game_button) and not self.is_in_air:
            self.is_in_air = True

        if self.is_in_air:
            self.next_frame_event.reset()
            self.time_in_air += VelocityCalculator.time
            self.animation_frame = self.jump_frame
            t = self.time_in_air
            self.top_edge = 1 / 2 * self.gravity * pow(t, 2) + self.upwards_velocity * t + self.initial_distance

        if self.top_edge > self.initial_distance:
            self.time_in_air = 0
            self.is_in_air = False
            self.top_edge = self.initial_distance
            self.animation_frame = 1

    def run_animation(self):
        self.next_frame_event.run(False, not self.is_in_air)

        if self.next_frame_event.is_done():
            self.animation_frame = (self.animation_frame + 1) % self.total_frames
            # self.next_frame_event.reset()
            overshoot_time = self.next_frame_event.current_time - self.next_frame_event.time_needed
            self.next_frame_event.current_time = overshoot_time

        self.path_to_image = f"{self.base_path}{self.animation_frame}.png"

    def reset(self):
        self.time_in_air, self.animation_frame = 0, 0
        self.next_frame_event.reset()
        self.left_edge = 0