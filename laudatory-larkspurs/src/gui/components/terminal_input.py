"""Terminal input widget for the terminal GUI."""

import re

from gui.element import Element, HTMLElement, Input

from .terminal_io import TerminalInputVerb


class TerminalInput(Element):
    """A terminal input component for user commands."""

    text_input: Input
    suggestion_span: Element
    input_wrapper: Element
    command_verb_span: TerminalInputVerb

    def __init__(self, parent: HTMLElement | Element | None = None) -> None:
        super().__init__(
            tag_name="div",
            parent=parent,
            id="terminal-input",
            style="""
            display: flex;
            flex-direction: row;
            align-items: center;
            flex-shrink: 0;
        """,
        )
        self.class_name = "terminal-input"
        self.text = "$ "

        self.input_wrapper = self._make_input_wrapper()
        self.suggestion_span = self._make_suggestion_span()
        self.suggestion_span.class_name = "suggestion-span"
        self.suggestion_span.text = ""

        self.command_verb_span = TerminalInputVerb(
            parent=self.input_wrapper,
            style="""
            background-color: transparent;
            font-family: monospace;
            position: absolute;
            left: 0;
            top: 0;
            font-size: 1rem;
            pointer-events: none;
            white-space: pre;
        """,
        )

        self.text_input = self._make_text_input()
        self.text_input.class_name = "terminal-text-input"

    def set_value(self, value: str) -> None:
        """Set the value of the text input."""
        self.text_input["value"] = value
        command = re.search(r"^(\s*)(\S+\b)", value)
        if not command:
            self.command_verb_span.set_text("", "")
            return
        self.command_verb_span.set_text(command.group(1), command.group(2))

    def _make_input_wrapper(self) -> Element:
        return Element(
            "div",
            parent=self,
            style="""
                position: relative;
                flex-grow: 1;
                width: 100%;
                display: flex;
                align-items: center;
            """,
        )

    def _make_suggestion_span(self) -> Element:
        return Element(
            "span",
            parent=self.input_wrapper,
            style="""
                background-color: transparent;
                color: var(--terminal-suggestion-color);
                font-family: monospace;
                position: absolute;
                left: 0;
                top: 0;
                width: 100%;
                font-size: 1rem;
                pointer-events: none;
                white-space: pre;
            """,
            id="suggestion-span",
        )

    def _make_text_input(self) -> Input:
        return Input(
            parent=self.input_wrapper,
            id="terminal-text-input",
            style="""
                width: 100%;
                font-family: monospace;
                background-color: transparent;
                color: var(--terminal-input-color);
                border: 0;
                outline: 0;
                margin: 0;
                padding: 0;
                font-size: 1rem;
                position: relative;
                z-index: 2;
            """,
            autocomplete="off",
        )

    def set_suggestion(self, suggestion: str | None) -> None:
        """Set the suggestion for the text input."""
        if not suggestion:
            self.suggestion_span.text = ""
            return
        self.suggestion_span.text = suggestion
