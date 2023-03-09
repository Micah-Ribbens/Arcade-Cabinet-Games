from gui_components.dimensions import Dimensions
from base.important_variables import game_window
from gui_components.component import Component
from base.utility_functions import *

class TextBox(Component):
    """A box that contains text. The background color, text color, text, font_size, and the text being centered can all be set"""

    text = ""
    font = None
    font_size = 0
    background_color = None
    text_color = None
    is_centered = False

    def __init__(self, text, font_size, background_color, text_color, is_centered):
        """ Initializes the object

            :parameter text: String; the text that is displayed
            :parameter font_size: int; the size of the font
            :parameter background_color: tuple; the (Red, Green, Blue) values of the text box's background
            :parameter text_color: tuple; the (Red, Green, Blue) values of the text's color
            :parameter is_centered: bool; whether the text inside the text box is centered

            :returns: None
        """

        super().__init__("")

        self.text, self.font_size = text, font_size
        self.text_color, self.is_centered = text_color, is_centered
        self.set_background_color(background_color)

        load_text(self.name, font_size, background_color, text_color)

        Dimensions.__init__(self, 0, 0, 0, 0)

    def render(self):
        """Renders the TextBox onto the screen"""

        super().render()

        left_edge, top_edge = self.left_edge, self.top_edge

        if self.is_centered:
            left_edge, top_edge = self.horizontal_midpoint, self.vertical_midpoint

        render_text(left_edge, top_edge, self.text_color, self.background_color, self.text, self.font_size, self.is_centered, self.name)
    def set_background_color(self, background_color):
        """Sets the background_color of the TextBox by setting 'self.color' and 'self.background_color' to the value provided ('background_color')"""

        self.color, self.background_color = background_color, background_color

    def set_text(self, text):
        """Sets TextBox 'self.text' attribute to 'text' """

        self.text = text