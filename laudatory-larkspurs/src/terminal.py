from commands import all_commands
from gui.components.terminal_gui import TerminalGui
from image import PaintImage
from utils.color import Color, create_color

SUCCESS_COLOUR = "var(--terminal-success-color)"
ERROR_COLOUR = "var(--terminal-error-color)"


def get_options(args: list[str]) -> tuple[list[str], dict[str, str]]:
    """Remove options from a given list of arguments."""
    options_start: int = 0
    while options_start < len(args) and not args[options_start].startswith("--"):
        options_start += 1

    options: dict[str, str] = {}
    last_key: str | None = None
    for arg in args[options_start:]:
        if arg.startswith("--"):
            last_key = arg[2:]
            options[last_key] = ""
            continue
        if options[last_key] != "":
            options[last_key] += " "
        options[last_key] += arg
    return args[:options_start], options


class Terminal:
    """Terminal manages a custom command environment.

    @author Philip
    """

    foreground_color = Color(255, 255, 255)
    background_color = Color(0, 0, 0)

    def __init__(self, image: PaintImage, display: TerminalGui) -> None:
        self.image = image

        self.terminal_display = display
        display.terminal = self

    def run_str(self, command_str: str) -> bool:
        """Parse and then run the given command.

        :param command_str: String of command to be executed
        :return: success of command execution

        @author Philip
        """
        if command_str.strip() == "":
            return False

        command: str
        args: list[str]
        command, *args = command_str.strip().split()

        options: dict[str, str | Color]
        args, options = get_options(args)

        if command in all_commands:
            command_obj = all_commands[command]
        else:
            self.output_error(f"`{command}` is not a valid command.")
            self.output_error("use `help` to see list of available commands`")
            return False

        invalid_options: tuple[str, ...] = tuple(
            option for option in options if option not in command_obj.known_options
        )

        if any(option not in command_obj.known_options for option in options):
            self.output_error(f"{invalid_options} are not a valid option(s) for the command.")
            return False

        try:
            if "fg" in command_obj.known_options:
                if "fg" in options:
                    options["fg"] = create_color(options["fg"])
                else:
                    options["fg"] = self.foreground_color
            if "bg" in command_obj.known_options:
                if "bg" in options:
                    options["bg"] = create_color(options["bg"])
                else:
                    options["bg"] = self.background_color

        except ValueError as e:
            self.output_error(e.args[0])
            return False

        command_obj(self, *args, **options)

        return True

    def predict_command(self, command_str: str) -> str | None:
        """Predicts the command and arguments the user is typing.

        Argument handling is offloaded to commands predict_args.

        :param command_str: Currently typed text in terminal.
        :return: The full predicted command with next argument. Returns None on error.

        @author Philip
        """
        if command_str.strip() == "":
            return ""

        command, *args = command_str.strip().split()

        args, options = get_options(args)

        if command in all_commands:
            output = command
            prediction = all_commands[command].predict_args(self, *args, **options)
            if prediction is None:
                return None
            if prediction == "":
                return command_str
            if not prediction.startswith(" "):
                args.pop()
                prediction = " " + prediction
            if args:
                output += " " + " ".join(args)
            output += prediction
            return output

        for full_command in all_commands:
            if full_command.startswith(command):
                return full_command
        return None

    def output_info(self, output: str) -> None:
        """Output the given input to the display with `info_colour`.

        :param output: Text to be printed
        :return: None

        @authors Philip
        """
        self.terminal_display.print_terminal_output(output)

    def output_success(self, output: str) -> None:
        """Output the given input to the display with `success_colour`.

        :param output: Text to be printed
        :return: None

        @author Philip
        """
        self.terminal_display.print_terminal_output(output, SUCCESS_COLOUR)

    def output_error(self, output: str) -> None:
        """Output the given input to the display with `error_colour`.

        :param output: Text to be printed
        :return: None

        @author Philip
        """
        self.terminal_display.print_terminal_output(output, ERROR_COLOUR)
