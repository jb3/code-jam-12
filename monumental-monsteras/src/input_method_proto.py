from collections.abc import Callable
from typing import Protocol

type TextUpdateCallback = Callable[[str], None]


class IInputMethod(Protocol):
    """An interface for any input method renderable in the WPM test page."""

    def on_text_update(self, callback: TextUpdateCallback) -> None:
        """Call `callback` every time the user input changes."""
        raise NotImplementedError
