import typing

from nicegui import ui

import input_method_proto


class SampleInputMethod(input_method_proto.IInputMethod):
    """A sample input method for basic reference.

    Consider using a dataclass instead with any complex state.
    """

    callbacks: list[typing.Callable[[str], None]]

    def __init__(self) -> None:
        self.callbacks = []
        self.inp = ui.input("input here")
        self.inp.on_value_change(lambda event: [x(event.value) for x in self.callbacks])

    def on_text_update(self, callback: typing.Callable[[str], None]) -> None:
        """Call `callback` every time the user input changes."""
        self.callbacks.append(callback)
