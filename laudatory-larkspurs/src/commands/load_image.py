from pathlib import Path
from typing import TYPE_CHECKING

from commands.base_command import BaseCommand

if TYPE_CHECKING:
    from terminal import Terminal

IMAGES_PATH = Path(__file__).parent.parent.resolve() / "images"


class LoadImage(BaseCommand):
    """load_image is a command that loads the given image.

    @author Mira
    """

    name: str = "load_image"
    help_pages: tuple[str, ...] = (
        """
        Usage: load_image <image_name.png>

        Default image loading: load_image default
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str, **_options: str) -> bool:
        """Load an image to program memory.

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: True if command was executed successfully.

        @author Mira
        """
        if not args:
            terminal.output_error("You need to provide a full image name. See help for more info.")
            return False
        if args[0] == "default":
            terminal.image.load()
            terminal.output_info("default image loaded")
        elif terminal.image.load(args[0]):
            terminal.output_error("Image not found.")
            return False
        terminal.output_info(f"image `{args[0]}` loaded")
        return True

    def predict_args(self, _terminal: "Terminal", *args: str, **_options: str) -> str | None:
        """Argument predictor."""
        if len(args) != 1:
            return ""
        for path in IMAGES_PATH.iterdir():
            if path.name.startswith(args[0]):
                return path.name
        return ""
