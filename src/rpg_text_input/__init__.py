from dataclasses import dataclass, field

from nicegui import ui
from nicegui.events import KeyEventArguments


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
class Keyboard:
    r"""A RPG-style keyboard where characters are selected by navigating with wasd/the arror keys.

    Positions are stored internally as (col, row).

    In the default keys list, \N{Squared Ok} is intended for once typing is complete,
    having to be pressed to complete the challenge.

    Raises:
        ValueError: If input keys is non-rectangular (jagged) or starting position is outside keys.

    """

    keys: tuple[str, ...] = (
        "ABCDEFGabcdefg",
        "HIJKLMNhijklmn",
        "OPQRSTUopqrstu",
        "VWXYZ. vwxyz,\N{SQUARED OK}",
    )

    position: list[int] = field(default_factory=lambda: [0, 0])

    def __post_init__(self) -> None:
        if not self.keys:
            msg = "Keyboard keys must not be empty."
            raise ValueError(msg)
        first_row_len = len(self.keys[0])
        for row in self.keys[1:]:
            if len(row) != first_row_len:
                msg = (
                    "All rows must be the same length, got"
                    f" {row!r} with length {len(row)} while expecting {first_row_len}."
                )
                raise ValueError(msg)
        if not (0 <= self.position[0] < len(self.keys[0])) or not (0 <= self.position[1] < len(self.keys)):
            msg = (
                f"Starting position {self.position} is outside bounds"
                f" (0, 0) to ({len(self.keys[0]) - 1}, {len(self.keys) - 1})"
            )
            raise ValueError(msg)

    @ui.refreshable_method
    def render(self) -> None:
        """Render the keyboard to the page."""
        with ui.grid(columns=len(self.keys[0])):
            for row_index, row in enumerate(self.keys):
                for col_index, char in enumerate(row):
                    label = ui.label(char if char != "`" else "")
                    label.style("text-align: center")
                    if [col_index, row_index] == self.position:
                        label.style("background-color: lightblue")

    def move(self, x: int, y: int) -> None:
        """Move the keyboard selected character in the given directions."""
        self.position[0] = wrap_to_range(self.position[0] + x, 0, len(self.keys[0]))
        self.position[1] = wrap_to_range(self.position[1] + y, 0, len(self.keys))
        self.render.refresh()

    def send_selected(self) -> None:
        """Send the selected character to the input view."""
        print(
            f"Selected {self.keys[self.position[1]][self.position[0]]!r}",
        )  # TODO(GiGaGon): Add communication with input view once it exists


@ui.page("/controller")
def rpg_text_input_page() -> None:
    """Page for the RPG style keyboard."""
    keyboard = Keyboard()
    keyboard.render()

    def handle_key(e: KeyEventArguments) -> None:
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
                keyboard.move(*direction)

        if e.key.code in {"Space", "Enter"}:
            keyboard.send_selected()

    ui.keyboard(on_key=handle_key)
