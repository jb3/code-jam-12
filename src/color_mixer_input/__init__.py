import string
from functools import partial

from nicegui import ui
from nicegui.events import ColorPickEventArguments
from src.input_method_proto import IInputMethod, TextUpdateCallback


class ColorInputComponent(IInputMethod):
    """Implements the color-based typing input page.

    Allows user to type using the color palette for letters, spaces, and backspaces, and UI buttons/switches for
    special characters ('.', '!', Shift, etc.)
    """

    def __init__(self) -> None:
        # typed_char is input displayed to user based on selected color
        # confirmed_char is character typed after user confirmation
        self.text_callback: TextUpdateCallback | None = None
        self.typed_text = ""
        self.typed_char = None
        self.confirmed_char = None
        self.selected_color = None
        self.shift_key_on = False
        (
            self.color_picker_row,
            self.color_label,
            self.input_label,
            self.command_buttons_row,
            self.special_char_buttons_row,
        ) = self.create_ui_content()
        self.setup_ui_buttons()

        self.color_dict = {
            "aqua": "#00FFFF",
            "blue": "#0000FF",
            "camouflage": "#3C3910",
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

    def on_text_update(self, callback: TextUpdateCallback) -> None:
        """Handle callbacks for text updates."""
        self.text_callback = callback

    def special_character_handler(self, char: str) -> None:
        """Handle special character events.

        This function handles special characters (e.g. '.', '!', ',', '?'). These characters are input using ui.button
        elements. Special characters are automatically output to the WPM  page.
        """
        self.selected_color = None
        self.typed_text += char
        self.typed_char = char
        self.confirmed_char = char
        self.update_helper_text()
        self.update_confirmation_text()

    def confirm_letter_handler(self) -> None:
        """Handle event when user clicks 'Confirm Letter'.

        After user clicks confirm, letter is typed and the WPM page updates the text.
        """
        alphabet = string.ascii_letters
        if self.typed_char in alphabet:
            self.confirmed_char = self.typed_char
            self.typed_text += self.confirmed_char
        self.update_confirmation_text()

    def color_handler(self, element: ColorPickEventArguments) -> None:
        """Handle events when user selects a color.

        Identifies closest color in dictionary. Maps that color to a letter or action.

        Black maps to backspace and white maps to space. Otherwise, colors map to the first letter of their name in the
        color dictionary.

        Letters must be confirmed by the user before being output to the WPM page. Special characters are automatically
        output to the WPM page.
        """
        print(type(element))
        selected_color_hex = element.color
        self.selected_color = self.find_closest_member(selected_color_hex)

        if self.selected_color == "black":
            self.typed_char = "backspace"
            if len(self.typed_text) > 0:
                self.typed_text = self.typed_text[:-1]
            self.confirmed_char = self.typed_char
        elif self.selected_color == "white":
            self.typed_text += " "
            self.typed_char = "space"
            self.confirmed_char = self.typed_char
        elif self.shift_key_on:
            self.typed_char = self.selected_color[0].upper()
        else:
            self.typed_char = self.selected_color[0]

        if self.typed_char in ["backspace", "space"]:
            self.update_confirmation_text()
        self.update_helper_text()

    def shift_handler(self) -> None:
        """Switch shift key on/off. The color_handler() method deals with capitalizing output."""
        self.shift_key_on = not self.shift_key_on

    def update_helper_text(self) -> None:
        """Update helper text on page.

        Displays the color and (if applicable) current character selected based on the user click."
        """
        self.color_label.text = f"Current Color: {self.selected_color}"
        self.input_label.text = f"Current Input: {self.typed_char}"
        self.color_label.update()
        self.input_label.update()

    def update_confirmation_text(self) -> None:
        """Update confirmed text on page.

        Display the confirmed character selected and all confirmed text typed thus far.

        """
        if self.text_callback:
            self.text_callback(self.typed_text)

    def create_ui_content(self) -> tuple[ui.row, ui.label, ui.label, ui.row, ui.row]:
        """Create the frame to hold the color picker, text labels, and buttons.

        Returns:
            tuple: (row for color picker, label for color selected, row for commands, row for special characters)

        """
        # Couldn't figure out how to position the palette so just stuck it in the page center.
        # It is on top of the wpm timer currently

        with ui.column().classes("absolute-center"):
            color_picker_row = ui.row()

        color_label = ui.label("Current Color: None")
        input_label = ui.label("Current Input:")
        command_buttons_row = ui.row().style("gap: 10px")
        special_char_buttons_row = ui.row().style("gap: 10x")
        return color_picker_row, color_label, input_label, command_buttons_row, special_char_buttons_row

    def setup_ui_buttons(self) -> None:
        """Create the buttons and other dynamic elements (e.g. labels, switches) on page."""
        with self.color_picker_row, ui.button(icon="colorize").style("opacity:0;pointer-events:none"):
            ui.color_picker(on_pick=self.color_handler, value=True).props("persistent")

        with self.command_buttons_row, ui.button_group().classes("gap-10"):
            ui.switch("CAPS LOCK", on_change=self.shift_handler).classes("bg-blue-500 text-white")
            ui.button("Confirm Letter", on_click=self.confirm_letter_handler).classes("bg-blue-500 text-white")

        with self.special_char_buttons_row, ui.button_group().classes("gap-10"):
            # creating wrappers to pass callback functions with parameters to buttons below
            callback_with_period = partial(self.special_character_handler, ".")
            callback_with_exclamation = partial(self.special_character_handler, "!")
            callback_with_comma = partial(self.special_character_handler, ",")
            callback_with_question_mark = partial(self.special_character_handler, "?")

            ui.button(".", on_click=callback_with_period).classes("bg-blue-500 text-white")
            ui.button("!", on_click=callback_with_exclamation).classes("bg-blue-500 text-white")
            ui.button(",", on_click=callback_with_comma).classes("bg-blue-500 text-white")
            ui.button("?", on_click=callback_with_question_mark).classes("bg-blue-500 text-white")

    @ui.page("/color_input")
    def color_input_page(self) -> None:
        """Create page displaying color_picker, character buttons, and text.

        This method allows the class to create a page separately from the WPM tester
        and was used for testing the class.
        """
        with ui.header():
            ui.label("Title text here?")

        with ui.left_drawer():
            ui.label("Special Keys:").style("font-weight:bold")
            ui.separator().style("opacity:0")
            ui.switch("CAPS LOCK", on_change=self.shift_handler)
            ui.button("Confirm Letter", on_click=self.confirm_letter_handler)
            ui.separator().props("color = black")

            # creating wrappers to pass callback functions with parameters to buttons below
            callback_with_period = partial(self.special_character_handler, ".")
            callback_with_exclamation = partial(self.special_character_handler, "!")
            callback_with_comma = partial(self.special_character_handler, ",")
            callback_with_question_mark = partial(self.special_character_handler, "?")

            ui.label("Special Characters:").style("font-weight:bold")
            ui.separator().style("opacity:0")
            with ui.grid(columns=2):
                ui.button(".", on_click=callback_with_period)
                ui.button("!", on_click=callback_with_exclamation)
                ui.button(",", on_click=callback_with_comma)
                ui.button("?", on_click=callback_with_question_mark)

        with ui.right_drawer():
            ui.label("Something could go here also")

        # ui labels displaying selected color, last input character, and text typed by user
        self.color_label.text = f"Color Selected: {self.selected_color}"
        self.input_label.text = f"Character Selected: {self.typed_char}"
        self.confirm_label.text = f"Character Typed: {self.confirmed_char}"
        self.text_label.text = f"Text Typed: {self.typed_text}"

        with ui.row(), ui.button(icon="colorize").style("opacity:0;pointer-events:none"):
            ui.color_picker(on_pick=self.color_handler, value=True).props("persistent")

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
            (key, ColorInputComponent.color_dist(color_hex, self.color_dict[key]), 2) for key in self.color_dict
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
        color_tuple_1 = ColorInputComponent.hex_to_rgb(color_code1)
        color_tuple_2 = ColorInputComponent.hex_to_rgb(color_code2)

        red_delta = color_tuple_1["red"] - color_tuple_2["red"]
        green_delta = color_tuple_1["green"] - color_tuple_2["green"]
        blue_delta = color_tuple_1["blue"] - color_tuple_2["blue"]

        return round((red_delta**2 + green_delta**2 + blue_delta**2) ** 0.5, 2)
