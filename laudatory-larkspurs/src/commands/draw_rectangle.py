import dataclasses
from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from utils.color import Color

if TYPE_CHECKING:
    from terminal import Terminal

REQUIRED_NUMBER_ARGS = 4


class DrawRectangle(BaseCommand):
    """Rectangle drawing on PaintImage.

    @author Mira
    """

    name: str = "draw_rectangle"
    help_pages: tuple[str, ...] = (
        """
        Usage: draw_rectangle <x> <y> <width> <height>

        arguments x,y: coordinate numbers
        arguments width,height: width and height of the rectangle
        """,
        """
        Options:
        fg <color>: set fill color for rectangle
        bg <color>: set border color for rectangle
        no-fill: don't fill rectangle
        outline <int>: set size of outline around rectangle
        """,
    )
    known_options = ("fg", "bg", "no-fill", "outline")

    def __call__(self, terminal: "Terminal", *args: str, **options: str | Color) -> bool:
        """Draw rectangle command.

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

        if not (args[2].isdigit() and args[3].isdigit()):
            terminal.output_error("Invalid size.")
            return False
        w, h = int(args[2]), int(args[3])

        if "no-fill" in options:
            fill_color = dataclasses.replace(options["fg"])
            fill_color.a = 0
        else:
            fill_color = options["fg"]

        if "outline" in options:
            if options["outline"].isdigit():
                outline_size = int(options["outline"])
                if outline_size < 0:
                    terminal.output_error("Invalid outline size.")
                    return False
                outline_color = options["bg"]
            else:
                terminal.output_error("Invalid outline size.")
                return False
        else:
            outline_size = 0
            outline_color = None

        terminal.image.fill_rect(x, y, w, h, fill_color, outline_color, outline_size)
        terminal.output_info(f"rectangle at {x}x{y} size {w}x{h} filled with rgb{options['fg'].rgba}")
        return True

    def predict_args(self, _terminal: "Terminal", *args: str, **_options: str | Color) -> str | None:
        """Argument predictor."""
        result = ""
        match len(args):
            case 0:
                result = " x"
            case 1:
                result = " y"
            case 2:
                result = " width"
            case 3:
                result = " height"
        return result
