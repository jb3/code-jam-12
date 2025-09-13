from typing import TYPE_CHECKING

from utils.color import Color

if TYPE_CHECKING:
    from terminal import Terminal


class BaseCommand:
    """BaseCommand is the class that all commands should inherit from.

    it contains some utility functions, but most calls should be overridden in full command implementation.

    `name` and `help_pages` should be overwritten in full command implementation.
    `known_options` is the options that a command can take.

    The options "fg" and "bg" are special and represent the foreground and background color for drawing.
    If these are requested, they will always be supplied
    either temporarily changed from command line or set from `fg` and `bg` commands.

    @author Philip
    """

    name: str = "BaseCommand"
    help_pages: tuple[str, ...] = (
        """BaseCommand is the class that all commands should inherit from.

        raises NotImplementedError when called as it and this message should never be seen.
        if you see this message in the application report how
        """,
    )
    known_options: tuple[str, ...] = ()

    def __call__(self, terminal: "Terminal", *args: str, **options: str | Color) -> bool:
        """Preforms the command being called using `*args`.

        This function should be overridden by subclasses.

        The subclasses implementation should handle argument handling.

        :param terminal: The terminal instance.
        :param args: Arguments passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: Was the command executed successfully?

        @author Philip
        """
        msg = "BaseCommand should not be called and should be overridden"
        raise NotImplementedError(msg)

    def predict_args(self, terminal: "Terminal", *args: str, **options: str | Color) -> str | None:
        """Predicts the next argument for the command.

        This function should be overridden by subclasses.

        The subclasses implementation should do error handling on incorrect arguments.

        :param terminal: The terminal instance.
        :param args: Arguments already passed to the command.
        :param options: Options passed to the command with optional arguments with those options.
        :return: The predicted continuance of the arguments for the command. If new argument, start with space.
                 If no more arguments "". If error in arguments, return None.

        @author Philip
        """
        msg = "BaseCommand should `predict_args` not be called and should be overridden"
        raise NotImplementedError(msg)
