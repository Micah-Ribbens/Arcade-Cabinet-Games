import random

from game_qu.base.engines import CollisionsEngine
from game_qu.base.important_variables import *
from game_qu.base.lines import Point, LineSegment
from game_qu.base.paths import Path
from game_qu.base.utility_functions import key_is_clicked
from game_qu.base.velocity_calculator import VelocityCalculator
from game_qu.gui_components.hud import HUD
from game_qu.gui_components.intermediate_screen import IntermediateScreen
from game_qu.gui_components.screen import Screen

from games.space_shooter.meteorite import Meteorite
from games.space_shooter.player import Player


class MeteoriteGameScreen(Screen):
    """A specific game mode in the entire space shooter game"""

    players = []
    is_versus = False

    time_between_meteorites = Path(Point(0, 4),[Point(1000, 3.5), Point(1500, 3.2), Point(2000, 3), Point(2500, 2.5), Point(3500, 1.6), Point(float("inf"), 1.6)])
    time_for_meteorites_to_fall = Path(Point(0, 5),[Point(1000, 5), Point(1500, 4.5), Point(2000, 3), Point(2500, 2.5), Point(3500, 2), Point(float("inf"), 2)])
    points_per_meteorite_destroyed = 200
    meteorites = []
    time_since_last_meteorite = 0
    number_of_players = 0
    player_total_score = 0
    player_scores = []
    high_score = 0
    game_is_reset = False

    intermediate_screen = None
    is_high_score = False
    hud = None

    def __init__(self, number_of_players, is_versus):
        """Initializes the screen with the game mode being decided by the parameters"""

        super().__init__("games/space_shooter/images/galaxy.png")
        self.is_versus = is_versus

        players_keys = [[KEY_A, KEY_D, KEY_W], [KEY_LEFT, KEY_RIGHT, KEY_UP]]
        self.players, self.meteorites, self.player_scores = [], [], []
        self.number_of_players = number_of_players

        for x in range(number_of_players):
            player_keys = players_keys[x]
            self.players.append(Player(player_keys[0], player_keys[1], player_keys[2], f"games/space_shooter/images/player{x + 1}.png", f"games/space_shooter/images/laser{x + 1}.png"))

        number_of_points_fields = number_of_players if is_versus else 1
        self.player_scores = [0] * number_of_points_fields
        self.hud = HUD(number_of_points_fields, [], SCREEN_LENGTH, SCREEN_HEIGHT * .1, 1, None, high_score_is_needed=True)

        self.create_meteorites()
        self.set_players_left_edge()
        self.intermediate_screen = IntermediateScreen(times_displayed=[1.2])

    def run(self):
        """Runs all the game logic"""

        if self.intermediate_screen.has_finished():
            self.run_meteorite_creation()
            self.hud.update(self.player_scores, self.high_score)
            self.update_scores()
            self.run_collisions()

        self.game_is_reset = False
        self.intermediate_screen.run()

    def run_meteorite_creation(self):
        """Runs all the logic for figuring out if a meteorite should be created"""

        self.time_since_last_meteorite += VelocityCalculator.time
        time_needed = self.time_between_meteorites.get_y_coordinate(self.player_total_score)
        player_has_created_meteorite = key_is_clicked(KEY_S) or key_is_clicked(KEY_DOWN)

        if player_has_created_meteorite:
            self.create_meteorite()
            self.time_since_last_meteorite = 0

        if self.time_since_last_meteorite >= time_needed:
            self.create_meteorites()
            self.time_since_last_meteorite = 0

    def create_meteorites(self):
        """Creates a meteorite for each player"""

        for x in range(self.number_of_players):
            self.create_meteorite()

    def create_meteorite(self):
        """Creates a meteorite with a random path"""

        min_left_edge = 0
        max_left_edge = int(SCREEN_LENGTH - Meteorite.length)

        start_left_edge = random.randint(min_left_edge, max_left_edge)
        max_change = SCREEN_LENGTH / 2

        min_end_left_edge = min_left_edge if start_left_edge - max_change < min_left_edge else start_left_edge - max_change
        max_end_left_edge = max_left_edge if start_left_edge + max_change > max_left_edge else start_left_edge + max_change

        end_left_edge = random.randint(int(min_end_left_edge), int(max_end_left_edge))
        meteorite_path = LineSegment(Point(start_left_edge, -Meteorite.height), Point(end_left_edge, SCREEN_HEIGHT - Meteorite.height))
        time_for_meteorite_to_fall = self.time_for_meteorites_to_fall.get_y_coordinate(self.player_total_score)
        self.meteorites.append(Meteorite(meteorite_path, time_for_meteorite_to_fall))

    def set_players_left_edge(self):
        """Resets the player's locations to their original location at the start of the game"""

        previous_player_left_edge = (SCREEN_LENGTH / 2) + Player.length * 1.5

        for player in self.players:
            player.left_edge = previous_player_left_edge - player.length * 1.5
            previous_player_left_edge = player.left_edge

    def update_scores(self):
        """Updates the scores of the players and the high score"""

        self.player_total_score = 0

        for player_score in self.player_scores:
            self.player_total_score += player_score

            if player_score > self.high_score:
                self.high_score = player_score
                self.is_high_score = True

    def run_collisions(self):
        """Runs all the collision logic between players, lasers, and meteorites"""

        alive_meteorites = []
        for meteorite in self.meteorites:
            if meteorite.bottom_edge >= SCREEN_HEIGHT:
                self.reset_game()

            if meteorite.hit_points <= 0:
                index_of_points = meteorite.last_player_hit_by if self.is_versus else 0
                self.player_scores[index_of_points] += self.points_per_meteorite_destroyed

            if meteorite.hit_points > 0:
                alive_meteorites.append(meteorite)

            self.run_meteorite_collisions(meteorite)

        if not self.game_is_reset:
            self.meteorites = alive_meteorites

    def run_meteorite_collisions(self, meteorite):
        """Runs all the collision logic between a meteorite and the players and their lasers"""

        for x in range(len(self.players)):
            player = self.players[x]
            alive_lasers = []

            if CollisionsEngine.is_collision(player, meteorite):
                self.reset_game()

            for laser in player.lasers:
                is_laser_collision = CollisionsEngine.is_collision(laser, meteorite)

                if is_laser_collision:
                    meteorite.hit_points -= laser.damage
                    meteorite.last_player_hit_by = x

                if laser.bottom_edge > 0 and not is_laser_collision:
                    alive_lasers.append(laser)

            player.lasers = alive_lasers

    def reset_game(self):
        """Resets the game to its original state"""

        self.display_message()
        self.meteorites = []
        self.player_total_score = 0
        self.create_meteorites()
        self.game_is_reset = True
        self.time_since_last_meteorite = 0

        for player in self.players:
            player.reset()

        self.set_players_left_edge()
        self.player_scores = [0] * len(self.player_scores)
        self.is_high_score = False

    def display_message(self):
        """Displays a message after the game is over for a short period of time"""

        message = self.get_versus_message() if self.is_versus else self.get_coop_message()

        self.intermediate_screen.set_texts([message])
        self.intermediate_screen.display()

    def get_versus_message(self):
        """
            Returns:
                str: The versus message that is displayed after the game is over
        """

        player_number_who_won = 0
        current_best_score = -1
        is_tie = True

        for x in range(len(self.player_scores)):
            player_score = self.player_scores[x]

            if player_score != current_best_score and current_best_score != -1:
                is_tie = False

            if player_score > current_best_score:
                current_best_score = player_score
                player_number_who_won = x + 1

        return f"Player #{player_number_who_won} Won" if not is_tie else f"It was a tie"

    def get_coop_message(self):
        """
            Returns:
                str: The cooperative message that is displayed after the game is over
        """

        message = f"You scored: {self.player_scores[0]}"

        if self.is_high_score:
            message = f"New High Score: {self.player_scores[0]}"

        return message

    def get_components(self):
        """
            Returns:
                list[Component]: The components that are displayed on the screen (either the game components or the
                intermediate screen text box)
        """

        player_components = []

        for player in self.players:
            player_components += player.get_components()

        game_components = [self.hud] + player_components + self.meteorites
        return self.intermediate_screen.get_components() if not self.intermediate_screen.has_finished() else game_components