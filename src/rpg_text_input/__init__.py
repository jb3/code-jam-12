from dataclasses import dataclass, field

from nicegui import ui


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

    def render(self) -> None:
        """Render the keyboard to the page."""
        with ui.grid(columns=len(self.keys[0])):
            for row_index, row in enumerate(self.keys):
                for col_index, char in enumerate(row):
                    label = ui.label(char if char != "`" else "")
                    label.style("text-align: center")
                    if [col_index, row_index] == self.position:
                        label.style("background-color: lightblue")


@ui.page("/controller")
def rpg_text_input_page() -> None:
    """Page for the RPG style keyboard."""
    keyboard = Keyboard()
    keyboard.render()
