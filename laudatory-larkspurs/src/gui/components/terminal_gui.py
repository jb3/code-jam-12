from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, Any

import js  # type: ignore[import]

from gui.element import Element, HTMLElement

from .terminal_input import TerminalInput
from .terminal_io import TerminalHistory, TerminalOutput, UserInput

if TYPE_CHECKING:
    from terminal import Terminal

KEYCODE_TAB = 9
KEYCODE_ENTER = 13


class CssVariable:
    """A class for managing a CSS variable for an Element."""

    name: str
    element: Element

    def __init__(self, name: str, element: Element) -> None:
        self.name = name
        self.element = element

    def get(self) -> str:
        """Get the value of the CSS variable."""
        return js.document.getComputedStyle(self.element.html_element).getPropertyValue(self.name)

    def set(self, value: str) -> None:
        """Set the value of the CSS variable."""
        self.element.html_element.style.setProperty(self.name, value)


class TerminalGui(Element):
    """The terminal GUI component for displaying terminal-like output and input."""

    max_previous_commands: int = 20
    previous_commands: deque[str]
    current_command_idx: int | None = None
    terminal: Terminal | None = None

    _output_color_variable: CssVariable
    _background_color_variable: CssVariable
    _success_color_variable: CssVariable
    _error_color_variable: CssVariable
    _suggestion_color_variable: CssVariable

    def get_suggestion(self, command: str | None) -> str | None:
        """Get a suggestion for the given command."""
        if not command:
            return None
        return self.terminal.predict_command(command)

    def print_terminal_output(self, text: str, color: str | None = None) -> None:
        """Print the given text to the terminal output."""
        output = TerminalOutput(text, color=color)
        self.history.add_history(output)

    def clear_terminal_history(self) -> None:
        """Clear the terminal history."""
        self.history.clear_history()
        self.input.set_suggestion(None)

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(
            tag_name="div",
            id="terminal",
            parent=parent,
            style="""
            background-color: var(--terminal-background-color);
            color: var(--terminal-output-color);
            flex-grow: 1;
            overflow-y: scroll;
            font-family: monospace;
            border: 0;
            outline: 0;
            margin: 0;
            padding: 20px;
            white-space: pre;
        """,
        )

        # Initialize CSS variables for terminal colors
        self._output_color_variable = CssVariable("--terminal-output-color", self)
        self._background_color_variable = CssVariable("--terminal-background-color", self)
        self._success_color_variable = CssVariable("--terminal-success-color", self)
        self._error_color_variable = CssVariable("--terminal-error-color", self)
        self._suggestion_color_variable = CssVariable("--terminal-suggestion-color", self)

        self.previous_commands = deque(maxlen=self.max_previous_commands)
        self.class_name = "terminal"

        self.history = TerminalHistory(parent=self)
        self.input = TerminalInput(parent=self)

        self.input.text_input.on("keydown", self._on_input_control_keydown)
        self.input.text_input.on("input", self._on_input)
        self.on("click", self._focus_input)

    @property
    def output_color(self) -> str:
        """The color of the terminal output."""
        return self._output_color_variable.get()

    @output_color.setter
    def output_color(self, value: str) -> None:
        self._output_color_variable.set(value)

    @property
    def background_color(self) -> str:
        """The background color of the terminal."""
        return self._background_color_variable.get()

    @background_color.setter
    def background_color(self, value: str) -> None:
        self._background_color_variable.set(value)

    @property
    def success_color(self) -> str:
        """The color used for successful terminal commands."""
        return self._success_color_variable.get()

    @success_color.setter
    def success_color(self, value: str) -> None:
        self._success_color_variable.set(value)

    @property
    def error_color(self) -> str:
        """The color used for error terminal commands."""
        return self._error_color_variable.get()

    @error_color.setter
    def error_color(self, value: str) -> None:
        self._error_color_variable.set(value)

    @property
    def suggestion_color(self) -> str:
        """The color used for terminal command suggestions."""
        return self._suggestion_color_variable.get()

    @suggestion_color.setter
    def suggestion_color(self, value: str) -> None:
        self._suggestion_color_variable.set(value)

    def _submit_input(self, event: Any) -> None:  # noqa: ANN401
        value = event.target.value
        self.history.add_history(UserInput(value))

        last_command = self.previous_commands[-1] if self.previous_commands else None
        if value and (last_command is None or value != last_command):
            self.previous_commands.append(value)

        if self.terminal is not None:
            self.terminal.run_str(value)
        else:
            print("Warning: TerminalGui has no Terminal instance assigned.")

        event.target.value = ""
        self.input.set_suggestion(None)
        self.input.set_value("")

    def _confirm_suggestion(self, event: Any) -> None:  # noqa: ANN401
        value = event.target.value
        self.input.set_value(self.get_suggestion(value) or value)

    def _navigate_commands(self, offset: int) -> None:
        if not self.previous_commands:
            return
        if self.current_command_idx is None:
            self.current_command_idx = len(self.previous_commands)
        self.current_command_idx = max(0, self.current_command_idx + offset)
        if self.current_command_idx >= len(self.previous_commands):
            self.current_command_idx = None
        if self.current_command_idx is None:
            self.input.set_value("")
        else:
            self.input.set_value(self.previous_commands[self.current_command_idx])

    def _on_input_control_keydown(self, event: Any) -> None:  # noqa: ANN401
        if event.keyCode == KEYCODE_ENTER:
            self._submit_input(event)
            self.current_command_idx = None
            event.preventDefault()
        elif event.keyCode == KEYCODE_TAB:
            self._confirm_suggestion(event)
            self.current_command_idx = None
            event.preventDefault()
        elif event.key == "ArrowUp":
            self._navigate_commands(-1)
            event.preventDefault()
        elif event.key == "ArrowDown":
            self._navigate_commands(1)
            event.preventDefault()
        elif event.key == "ArrowRight" and event.target.selectionStart == len(event.target.value):
            self._confirm_suggestion(event)
            self.current_command_idx = None
            event.preventDefault()

    def _on_input(self, event: Any) -> None:  # noqa: ANN401
        self.input.set_suggestion(self.get_suggestion(event.target.value))
        self.input.set_value(event.target.value)
        self.current_command_idx = None

    def _focus_input(self, _event: Any) -> None:  # noqa: ANN401
        if len(js.window.getSelection().toString()) > 0:
            return
        self.input.text_input["focus"]()
