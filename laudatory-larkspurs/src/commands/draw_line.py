from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from utils.color import Color

if TYPE_CHECKING:
    from terminal import Terminal

REQUIRED_NUMBER_ARGS = 4


class DrawLine(BaseCommand):
    """Line drawing on PaintImage.

    @author Mira
    """

    name: str = "draw_line"
    help_pages: tuple[str, ...] = (
        """
        Usage: draw_line <x1> <y1> <x2> <y2>

        arguments x1,y1: starting coordinates
        arguments x2,y2: ending coordinates
        argument color: color name
        arguments r,g,b: red,green,blue numbers
        """,
        """
        Options:
        fg <color>: set color of line
        """,
    )
    known_options = ("fg",)

    def __call__(self, terminal: "Terminal", *args: str, **options: str | Color) -> bool:
        """Draw line command.

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
            terminal.output_error("Invalid starting coordinates.")
            return False
        if not (
            args[2].isdigit() and args[3].isdigit() and 0 <= int(args[2]) < size[0] and 0 <= int(args[3]) < size[1]
        ):
            terminal.output_error("Invalid ending coordinates.")
            return False

        x1, y1 = int(args[0]), int(args[1])
        x2, y2 = int(args[2]), int(args[3])

        terminal.image.draw_line(x1, y1, x2, y2, options["fg"])
        terminal.output_info(f"line from {x1}x{y1} to {x2}x{y2} with rgb{options['fg'].rgba}")
        return True

    def predict_args(self, _terminal: "Terminal", *args: str, **_options: str | Color) -> str | None:
        """Argument predictor."""
        result = ""
        match len(args):
            case 0:
                result = " x1"
            case 1:
                result = " y1"
            case 2:
                result = " x2"
            case 3:
                result = " y2"
        return result
