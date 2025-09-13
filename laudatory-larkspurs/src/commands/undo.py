from typing import TYPE_CHECKING

from commands.base_command import BaseCommand

if TYPE_CHECKING:
    from terminal import Terminal


class Undo(BaseCommand):
    """Magic Undo button.

    @author Mira
    """

    name: str = "undo"
    help_pages: tuple[str, ...] = (
        """
        Usage: undo

        Undoes the last thing you did.
        Can be only done once!
        """,
    )

    def __call__(self, terminal: "Terminal", *_args: str, **_options: str) -> bool:
        """...

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: True if command was executed successfully.

        @author Mira
        """
        if terminal.image.undo():
            terminal.output_error("Cannot be undone.")
            return False
        terminal.output_success("Undone :)")
        return True

    def predict_args(self, _terminal: "Terminal", *_args: str, **_options: str) -> str | None:
        """Argument predictor."""
        return ""
