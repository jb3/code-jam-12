from pathlib import Path
from string import ascii_letters, digits
from typing import TYPE_CHECKING

from commands.base_command import BaseCommand

if TYPE_CHECKING:
    from terminal import Terminal

IMAGES_PATH = Path(__file__).parent.parent.resolve() / "images"


class SaveImage(BaseCommand):
    """...

    @author Mira
    """

    name: str = "save_image"
    help_pages: tuple[str, ...] = (
        """
        Usage: save_image <image_name.png>

        Allowed characters: A-Z a-z 0-9 _

        flags:
        --overwrite overwrites previous image
        """,
    )

    def __call__(self, terminal: "Terminal", *args: str, **_options: str) -> bool:
        """...

        :param terminal: The terminal instance.
        :param args: Arguments to be passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: True if command was executed successfully.

        @author Mira
        """
        if len(args) == 0:
            terminal.output_error("You need to provide a full image name. See help for more info.")
            return False
        if len(args) > 1:
            terminal.output_error("Too many arguments. See help for more info.")
            return False
        path = args[0]
        if not path.endswith(".png"):
            terminal.output_error("Please save the image as a .png")
            return False
        for character in path[:-4]:
            if character not in ascii_letters + digits + "_":
                terminal.output_error("Invalid characters in Image name.")
                terminal.output_error("Please check `help save_image` for more information.")
                return False
        if (IMAGES_PATH / path).exists() and not args.__contains__("--overwrite"):
            terminal.output_error("This path already exists, use --overwrite to overwrite it")
            return False
        terminal.image.save(path)
        terminal.output_info(f"Image succesfully saved as `{path}`")
        return True

    def predict_args(self, _terminal: "Terminal", *args: str, **_options: str) -> str | None:
        """Argument predictor."""
        if len(args) > 2 or len(args) == 0:  # noqa: PLR2004
            return ""
        if args[0].endswith(".png"):
            if (IMAGES_PATH / args[0]).exists():
                return args[0] + " --overwrite"
            return ""
        for path in IMAGES_PATH.iterdir():
            if path.name.startswith(args[0]):
                return path.name + " --overwrite"
        return args[0].split(".")[0] + ".png"
