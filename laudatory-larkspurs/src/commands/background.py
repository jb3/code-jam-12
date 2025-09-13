from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from utils.color import create_color

if TYPE_CHECKING:
    from terminal import Terminal


class Background(BaseCommand):
    """Sets the background color for use in drawing commands.

    @author Philip
    """

    name: str = "bg"
    help_pages: tuple[str, ...] = (
        """Sets the background color for use in drawing commands.

        Usage: bg <color>
        Examples:
        bg 255 255 255
        bg 100 0 0 255
        bg gold
        bg #C0FFEE
        bg rgb(0 200 150)
        bg rgba(0 255 255 100)
        bg hsv(360 100 100)
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str, **_options: str) -> bool:
        """Set the background color for use in drawing commands.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: True if command was executed successfully.

        @author Philip
        """
        try:
            color = create_color(" ".join(args))
        except ValueError as e:
            terminal.output_error(e.args[0])
            return False

        terminal.background_color = color

        return True

    def predict_args(self, terminal: "Terminal", *args: str, **_options: str) -> str | None:
        """Predicts the next argument for help.

        :param terminal: The terminal instance.
        :param args: Arguments already passed to the command.
        :return: The predicted continuance of the arguments for the command. If new argument, start with space.
                 If no more arguments "". If error in arguments, return None.

        @author Philip
        """
        if not all(arg.isdigit() for arg in args):
            return ""

        match len(args):
            case 0:
                return " " + str(terminal.background_color.r)
            case 1:
                return " " + str(terminal.background_color.g)
            case 2:
                return " " + str(terminal.background_color.b)
            case 3:
                return " " + str(terminal.background_color.a)

        return None
