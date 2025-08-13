# noqa: N999
from functools import partial

from nicegui import ui
from nicegui.events import ColorPickEventArguments

# Note: Most onscreen updates include pop-up notifications via ui.notify(). These were used to assist debugging
# but can/will be removed later


class ColorInputManager:
    """Implements the color-based typing input page.

    Allows user to type using the color palette for letters, spaces, and backspaces, and UI buttons/switches for
    special characters ('.', '!', Shift, etc.)
    """

    def __init__(self) -> None:
        self.typed_text = ""
        self.typed_char = None
        self.selected_color = None
        self.shift_key_on = False
        self.color_label = ui.label("None")
        self.input_label = ui.label("None")
        self.text_label = ui.label("None")
        self.color_dict = {
            "aqua": "#00FFFF",
            "blue": "#0000FF",
            "cyan": "#00FFFF",
            "darkblue": "#00008B",
            "emerald": "00674F",
            "fuchsia": "#FF00FF",
            "gray": "#7F7F7F",
            "hotpink": "#FF69B4",
            "indigo": "#4B0082",
            "jasmine": "#F8DE7E",
            "khaki": "#F0E68C",
            "lime": "#00FF00",
            "maroon": "#800000",
            "navy": "#000080",
            "orange": "#FFA500",
            "purple": "#800080",
            "quicksilver": "#A6A6A6",
            "red": "#FF0000",
            "salmon": "#FA8072",
            "teal": "#008080",
            "ube": "#8878C3",
            "viridian": "#40826D",
            "walnut": "#773F1A",
            "xanadu": "#738678",
            "yellow": "#FFFF00",
            "zara": "#B48784",
            "black": "#000000",
            "white": "#FFFFFF",
        }

    def special_character_handler(self, char: str) -> None:
        """Handle special character events.

        This function handles special characters (e.g. '.', '!', ',', '?'). These characters are input using ui.button
        elements.
        """
        self.typed_text += char
        self.typed_char = char
        ui.notify(f"Previous input: {self.typed_char} , typed text: {self.typed_text}")
        self.update_text(self.typed_text, "None", char)

    def color_handler(self, element: ColorPickEventArguments) -> None:
        """Handle events when user selects a color.

        Identifies closest color in dictionary and maps that color to a text output that is displayed to the user.
        Black maps to backspace and white maps to space. Otherwise, colors map to the first letter of their name in the
        color dictionary.
        """
        print(type(element))
        selected_color_hex = element.color
        self.selected_color = self.find_closest_member(selected_color_hex)
        if self.selected_color == "black":
            self.typed_char = "backspace"
            if len(self.typed_text) > 0:
                self.typed_text = self.typed_text[:-1]
        elif self.selected_color == "white":
            self.typed_char = "space"
            self.typed_text += " "
        else:
            if self.shift_key_on:
                self.typed_char = self.selected_color[0].upper()
            else:
                self.typed_char = self.selected_color[0]
            self.typed_text += self.typed_char
        ui.notify(f"Color: {self.selected_color}, Previous input: {self.typed_char}, typed text: {self.typed_text}")
        self.update_text(self.typed_text, self.selected_color, self.typed_char)

    def shift_handler(self) -> None:
        """Switch shift key on/off. The color_handler() method deals with capitalizing output."""
        self.shift_key_on = not self.shift_key_on

    def update_text(self, typed_txt: str, color_txt: str, input_txt: str) -> None:
        """Update text on page.

        Page displays the last color selected, the last character input, and the current string user has typed. If a
        special character was selected the last color selected is "None."

        :param typed_txt: string representing what user has typed so far
        :param color_txt: last color selected by user
        :param input_txt: last character input by user
        :return: None
        """
        self.color_label.text = f"Selected Color: {color_txt}"
        self.input_label.text = f"Previous Input: {input_txt}"
        self.text_label.text = f"Typed Text: {typed_txt}"
        self.color_label.update()
        self.input_label.update()
        self.text_label.update()

    @ui.page("/color_input")
    def color_input_page(self) -> None:
        """Create page displaying color_picker, character buttons, and text."""
        with ui.header():
            ui.label("Title text here?")

        with ui.left_drawer():
            ui.label("Description or instructions here?")
            ui.separator().props("color = black")
            ui.switch("SHIFT", on_change=self.shift_handler)
            ui.separator().props("color = black")

            # creating wrappers to pass callback functions with parameters to buttons below
            callback_with_period = partial(self.special_character_handler, ".")
            callback_with_exclamation = partial(self.special_character_handler, "!")
            callback_with_comma = partial(self.special_character_handler, ",")
            callback_with_question_mark = partial(self.special_character_handler, "?")

            ui.label("Special Characters:")
            with ui.grid(columns=2):
                ui.button(".", on_click=callback_with_period)
                ui.button("!", on_click=callback_with_exclamation)
                ui.button(",", on_click=callback_with_comma)
                ui.button("?", on_click=callback_with_question_mark)

        with ui.right_drawer():
            ui.label("Something could go here also")

        # ui labels displaying selected color, last input character, and text typed by user
        with ui.row():  # .classes('w-full border')
            self.color_label.text = f"Selected Color: {self.selected_color}"
            self.input_label.text = f"Previous Input: {self.typed_char}"
            self.text_label.text = f"Typed Text: {self.typed_text}"

        with ui.row(), ui.button(icon="colorize"):
            # color picker currently disappears if user clicks outside of palette
            # no-parent-event toggle does not fix this as it only applies to immediate parent not entire screen
            # as is user can reopen color palette by pressing the button again
            ui.color_picker(on_pick=self.color_handler, value=True)  # .props('no-parent-event')

        ui.run()

    def find_closest_member(self, color_hex: str) -> str:
        """Compare color hexcode to each color in class dicitionary. Return closest color.

        Takes a color hexcode and compares it to all colors in the class dictionary, finding the "closest" color
        in the dictionary. Uses the Euclidean distance metric on the RGB values of the hexcode to compute distance.
        The function returns the key of the most similar dict entry, which is the name of a color name (string).

        :param color_hex: a color hexcode
        :return: name (string) of the color with the closest hexcode
        """
        color_dists = [
            (key, ColorInputManager.color_dist(color_hex, self.color_dict[key]), 2) for key in self.color_dict
        ]
        color_dists = sorted(color_dists, key=lambda e: e[1])

        return color_dists[0][0]

    # Static methods below

    @staticmethod
    def hex_to_rgb(color_hex: str) -> dict[str, int]:
        """Return dictionary of RGB color values from color hexcode.

        Takes a color hexcode and returns a dictionary with (color,intensity)
        key/value pairs for Red, Green, and Blue

        :param color_hex: string representing a color hexcode
        :return: dictionary of color:intensity pairs
        """
        hex_code_length = 6
        invalid_code = "Invalid color code"
        if color_hex[0] == "#":
            color_hex = color_hex[1:]
        if len(color_hex) != hex_code_length:
            raise ValueError(invalid_code)

        red_val = int(color_hex[0:2], 16)
        green_val = int(color_hex[2:4], 16)
        blue_val = int(color_hex[4:6], 16)
        return {"red": red_val, "green": green_val, "blue": blue_val}

    @staticmethod
    def color_dist(color_code1: str, color_code2: str) -> float:
        """Return distance between two colors using their RGB values.

        Takes two hex_color codes and returns the "distance" between the colors. The distance is computed using the
        Euclidean distance metric by treating the colors 3-tuples (RGB). Rounds to two decimal places.

        :param color_code1: string representing a color hexcode
        :param color_code2: string representing a color hexcode
        :return: float representing Euclidean distance between colors
        """
        color_tuple_1 = ColorInputManager.hex_to_rgb(color_code1)
        color_tuple_2 = ColorInputManager.hex_to_rgb(color_code2)

        red_delta = color_tuple_1["red"] - color_tuple_2["red"]
        green_delta = color_tuple_1["green"] - color_tuple_2["green"]
        blue_delta = color_tuple_1["blue"] - color_tuple_2["blue"]

        return round((red_delta**2 + green_delta**2 + blue_delta**2) ** 0.5, 2)


# Create page using code below
color_page = ColorInputManager()
color_page.color_input_page()
