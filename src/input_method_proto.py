import typing


class IInputMethod(typing.Protocol):
    """An interface for any input method renderable in the WPM test page."""

    def on_text_update(self, callback: typing.Callable[[str], None]) -> None:
        """Call `callback` every time the user input changes."""
        raise NotImplementedError
