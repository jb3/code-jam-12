from typing import TYPE_CHECKING

from commands.base_command import BaseCommand

if TYPE_CHECKING:
    from terminal import Terminal


class ImageInfo(BaseCommand):
    """Display Image info.

    @author Mira
    """

    name: str = "image_info"
    help_pages: tuple[str, ...] = (
        """
        Usage: image_info
        or you can get specific pixel info: image_info <x> <y>
        No arguments.
        Displays: size, number of colors
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
        info = terminal.image.get_info()
        if len(args) == 2:  # noqa: PLR2004
            # check if the pixel is in an image
            if (
                args[0].isdigit()
                and args[0].isdigit()
                and 0 <= int(args[0]) < info["size"][0]
                and 0 <= int(args[1]) < info["size"][1]
            ):
                terminal.output_info(f"Image pixel info (x:{int(args[0])} y:{int(args[1])}):")
                terminal.output_info(f"Color: rgb{terminal.image.get_pixel(int(args[0]), int(args[1]))}")
                return True
            terminal.output_error("Incorrectly placed x and y coordinates of a pixel.")
            return False
        terminal.output_info("Image info:")
        terminal.output_info(f"Size: {info['size'][0]}x{info['size'][1]} pixels")
        terminal.output_info(f"Edit count: {info['edits']}")
        if info["colors"]:
            terminal.output_info(f"Colors: {len(info['colors'])}")
        return True

    def predict_args(self, _terminal: "Terminal", *args: str, **_options: str) -> str | None:
        """Argument predictor."""
        if len(args) == 0:
            return " x y"
        if len(args) == 1:
            return " y"
        return ""
