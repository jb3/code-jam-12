from dataclasses import dataclass
from typing import override

from nicegui import ui
from nicegui.events import KeyEventArguments

import config
from input_method_proto import IInputMethod, TextUpdateCallback


def wrap_to_range(num: int, num_min: int, num_max: int) -> int:
    """Ensure num is in the half-open interval [min, max), wrapping as needed.

    Returns:
        The input num wrapped to the given range.

    Raises:
        ValueError: If min is greater than or equal to max.

    """
    if num_min >= num_max:
        msg = f"Wrapping doesn't make sense if min >= max, got {num_min=} and {num_max=}."
        raise ValueError(msg)
    while num < num_min:
        num += num_max
    while num >= num_max:
        num -= num_max
    return num


@dataclass
class WrappingPosition:
    """X and Y position with wrapping addition."""

    x: int
    y: int
    max_x: int
    max_y: int

    def wrapping_add(self, x: int, y: int) -> "WrappingPosition":
        """Add an X and a Y to self, wrapping as needed."""
        new_x = wrap_to_range(self.x + x, 0, self.max_x)
        new_y = wrap_to_range(self.y + y, 0, self.max_y)
        return WrappingPosition(new_x, new_y, self.max_x, self.max_y)


KEYBOARD_KEYS: tuple[str, ...] = (
    "ABCDEFGabcdefg",
    "HIJKLMNhijklmn",
    "OPQRSTUopqrstu",
    "VWXYZ. vwxyz!\N{SYMBOL FOR BACKSPACE}",
)


class Keyboard(IInputMethod):
    r"""A RPG-style keyboard where characters are selected by navigating with wasd/the arror keys.

    Positions are stored internally as (col, row).

    Raises:
        ValueError: If input keys is non-rectangular (jagged) or starting position is outside keys.

    """

    def __init__(self) -> None:
        self.position: WrappingPosition = WrappingPosition(0, 0, len(KEYBOARD_KEYS[0]), len(KEYBOARD_KEYS))
        self.callbacks: list[TextUpdateCallback] = []
        self.text: str = ""

        self.render()
        ui.keyboard(on_key=self.handle_key)

    @ui.refreshable_method
    def render(self) -> None:
        """Render the keyboard to the page."""
        with (
            ui.element("div").classes("w-full h-full flex justify-center items-center"),  # centering div
            ui.element("div").classes(
                f"w-[85%] h-[60%] bg-[{config.COLOR_STYLE['primary_bg']}] p-5 rounded-xl"
            ),  # keyboard outer
            ui.grid(columns=len(KEYBOARD_KEYS[0])).classes("h-full w-full"),  # key grid
        ):
            for row_index, row in enumerate(KEYBOARD_KEYS):
                for col_index, char in enumerate(row):
                    with ui.element("div").classes(  # keys
                        f"w-full h-full flex justify-center items-center border-2 "
                        f"{
                            'bg-[' + config.COLOR_STYLE['primary'] + ']'
                            if (col_index, row_index) == (self.position.x, self.position.y)
                            else 'bg-[' + config.COLOR_STYLE['secondary_bg'] + ']'
                        } "
                        f"border-[{config.COLOR_STYLE['secondary_bg']}] rounded-md"
                    ):
                        (
                            ui.label(char)
                            .style("font-size: clamp(1rem, 3vh, 3rem)")
                            .classes(f"text-center text-[{config.COLOR_STYLE['contrast']}] p-2")
                        )

    def move(self, x: int, y: int) -> None:
        """Move the keyboard selected character in the given directions."""
        self.position = self.position.wrapping_add(x, y)
        self.render.refresh()

    def send_selected(self) -> None:
        """Send the selected character to the input view."""
        key = KEYBOARD_KEYS[self.position.y][self.position.x]
        if key != "\N{SYMBOL FOR BACKSPACE}":
            self.text += key
        else:
            self.text = self.text[:-1]

        for callback in self.callbacks:
            callback(self.text)

    def handle_key(self, e: KeyEventArguments) -> None:
        """Input handler for the RPG style keyboard."""
        if not e.action.keydown:
            return

        # Done using a for loop to minimize copy/paste errors
        for key_codes, direction in (
            ({"KeyW", "ArrowUp"}, (0, -1)),
            ({"KeyS", "ArrowDown"}, (0, 1)),
            ({"KeyA", "ArrowLeft"}, (-1, 0)),
            ({"KeyD", "ArrowRight"}, (1, 0)),
        ):
            if e.key.code in key_codes:
                self.move(*direction)

        if e.key.code in {"Space", "Enter"}:
            self.send_selected()

    @override
    def on_text_update(self, callback: TextUpdateCallback) -> None:
        self.callbacks.append(callback)
