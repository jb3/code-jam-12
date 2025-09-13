from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from utils.color import Color

if TYPE_CHECKING:
    from terminal import Terminal

REQUIRED_NUMBER_ARGS = 6


class DrawPolygon(BaseCommand):
    """Polygon drawing on PaintImage.

    @author Philip
    """

    name: str = "draw_polygon"
    help_pages: tuple[str, ...] = (
        """
        Usage: draw_rectangle <x1> <y1> <x2> <y2> <x3> <y3> ...

        arguments x,y: coordinate numbers for points on polygon
        Requires at least 3 points and even number of arguments
        """,
        """
        Options:
        fg <color>: set fill color for polygon
        bg <color>: set border color for polygon
        no-fill: don't fill polygon
        outline <int>: set size of outline around polygon
        """,
    )
    known_options = ("fg", "bg", "no-fill", "outline")

    def __call__(self, terminal: "Terminal", *args: str, **options: str | Color) -> bool:
        """Draw polygon command.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: True if command was executed successfully.

        @author Mira
        """
        if len(args) < REQUIRED_NUMBER_ARGS and len(args) % 2 == 0:
            terminal.output_error("Bad amount of arguments, see help for options")
            return False

        size = terminal.image.img.size
        points: list[tuple[int, int]] = []
        for x, y in zip(args[::2], args[1::2], strict=False):
            if not (x.isdigit() and y.isdigit() and 0 <= int(x) < size[0] and 0 <= int(y) < size[1]):
                terminal.output_error(f"Invalid coordinates: ({x}, {y})")
                return False
            points.append((int(x), int(y)))

        fill_color = None if "no-fill" in options else options["fg"]

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

        terminal.image.draw_polygon(points, fill_color, outline_color, outline_size)
        terminal.output_info(f"drawn {len(points)}-sided polygon filled with rgba{fill_color.rgba}")
        return True

    def predict_args(self, _terminal: "Terminal", *args: str, **_options: str | Color) -> str | None:
        """Argument predictor."""
        return " x" if len(args) % 2 == 0 else " y"
