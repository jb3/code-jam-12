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
    """On-screen keyboard input method."""

    keys: tuple[str, ...] = (
        "ABCDEFGabcdefg",
        "HIJKLMNhijklmn",
        "OPQRSTUopqrstu",
        "VWXYZ. vwxyz,\N{SQUARED OK}",
    )

    position: list[int] = field(default_factory=lambda: [0, 0])

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
