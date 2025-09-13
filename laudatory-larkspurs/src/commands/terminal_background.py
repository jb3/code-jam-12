from typing import TYPE_CHECKING

from commands.base_command import BaseCommand
from utils.color import create_color

if TYPE_CHECKING:
    from terminal import Terminal


class TerminalBackground(BaseCommand):
    """terminal_background is a command that changes background color of the terminal.

    @author Julien
    """

    name: str = "terminal_background"
    help_pages: tuple[str, ...] = (
        """terminal_background is a command that changes background color of the terminal.

        Usage: terminal_background <color>
        Exemple: bg rgb(255, 100, 0)
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str, **_options: str) -> bool:
        """Change the background color of the web page.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: True if command was executed successfully.

        @author Julien
        """
        try:
            terminal.terminal_display.background_color = f"rgb{create_color(' '.join(args)).rgb}"
        except ValueError as e:
            terminal.output_error(e.args[0])
            return False

        terminal.output_info("background-color succesfully changed")
        return True
