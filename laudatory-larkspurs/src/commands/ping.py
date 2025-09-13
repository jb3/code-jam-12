from typing import TYPE_CHECKING

from commands.base_command import BaseCommand

if TYPE_CHECKING:
    from terminal import Terminal


class Ping(BaseCommand):
    """Test ping command.

    Just echos pong to terminal

    @author Philip
    """

    name: str = "ping"
    help_pages: tuple[str, ...] = (
        """Pong!!!
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str, **_options: str) -> bool:
        """Print pong to terminal.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: True if command was executed successfully.

        @author Philip
        """
        terminal.output_success("pong" + (f": {', '.join(args)}" if args else ""))
        return True

    def predict_args(self, _terminal: "Terminal", *_args: str, **_options: str) -> str | None:
        """Argument predictor."""
        return ""
