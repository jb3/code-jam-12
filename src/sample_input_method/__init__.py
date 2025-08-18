from typing import override

from nicegui import ui

from input_method_proto import IInputMethod, TextUpdateCallback


class SampleInputMethod(IInputMethod):
    """A sample input method for basic reference.

    Consider using a dataclass instead with any complex state.
    """

    callbacks: list[TextUpdateCallback]

    def __init__(self) -> None:
        self.callbacks = []
        self.inp = ui.input("input here")
        self.inp.on_value_change(lambda event: [x(event.value) for x in self.callbacks])

    @override
    def on_text_update(self, callback: TextUpdateCallback) -> None:
        """Call `callback` every time the user input changes."""
        self.callbacks.append(callback)
