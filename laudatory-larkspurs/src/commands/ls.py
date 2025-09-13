from pathlib import Path
from typing import TYPE_CHECKING

from commands.base_command import BaseCommand

if TYPE_CHECKING:
    from terminal import Terminal

IMAGES_PATH = Path(__file__).parent.parent.resolve() / "images"


class Ls(BaseCommand):
    """Listing of image directory.

    @author Mira
    """

    name: str = "ls"
    help_pages: tuple[str, ...] = (
        """
        Usage: ls

        Lists the directory of images.
        Does not need any arguments.
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str, **_options: str) -> bool:
        """List all image files.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: True if command was executed successfully.

        @author Mira
        """
        if args:
            terminal.output_error("No arguments needed")
        terminal.output_info("Files: " + " ".join([path.name for path in IMAGES_PATH.iterdir() if path.is_file()]))
        return True

    def predict_args(self, _terminal: "Terminal", *_args: str, **_options: str) -> str | None:
        """Argument predictor."""
        return ""
