from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from utils.color import Color

if TYPE_CHECKING:
    from terminal import Terminal

REQUIRED_NUMBER_ARGS = 2


class DrawPixel(BaseCommand):
    """Pixel drawing on PaintImage.

    @author Mira
    """

    name: str = "draw_pixel"
    help_pages: tuple[str, ...] = (
        """
        Usage: draw_pixel <x> <y>

        arguments x,y: coordinate numbers
        """,
        """
        Options:
        fg <color>: set color of pixel
        """,
    )
    known_options = ("fg",)

    def __call__(self, terminal: "Terminal", *args: str, **options: str | Color) -> bool:
        """Draw pixel command.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: True if command was executed successfully.

        @author Mira
        """
        if len(args) != REQUIRED_NUMBER_ARGS:
            terminal.output_error("Bad amount of arguments, see help for options")
            return False

        size = terminal.image.img.size
        if not (
            args[0].isdigit() and args[1].isdigit() and 0 <= int(args[0]) < size[0] and 0 <= int(args[1]) < size[1]
        ):
            terminal.output_error("Invalid coordinates.")
            return False
        x, y = int(args[0]), int(args[1])

        terminal.image.set_pixel(x, y, options["fg"])
        terminal.output_info(f"Pixel at {x}x{y} filled with rgb{options['fg'].rgba}.")
        return True

    def predict_args(self, _terminal: "Terminal", *args: str, **_options: str) -> str | None:
        """Argument predictor."""
        result = ""
        match len(args):
            case 0:
                result = " x"
            case 1:
                result = " y"
        return result
