from dataclasses import dataclass

from nicegui import ui

import input_method_proto
import input_view
import sample_input_method


def get_input_method_by_name(inmth: str) -> type[input_method_proto.IInputMethod] | None:
    """Get an input method class by it's name.

    :returns: `type[IInputMethod]` on success, `None` on failure.
    """
    if inmth == "sample":
        return sample_input_method.SampleInputMethod
    return None


@dataclass
class WpmTesterPageState:
    """The page state."""

    """Useless for now, may be useful later?"""
    text: str


async def wpm_tester_page(method: str) -> None:
    """Create the actual page which tests the wpm.

    Usage:
        In main.py, use @ui.page("/test/{method}")(this) then this takes
        the method from the url
    """
    state = WpmTesterPageState("")

    input_method_def = get_input_method_by_name(method)
    if input_method_def is None:
        ui.navigate.to("/")
        return

    with ui.header(elevated=True).classes("align-center justify-center"):
        ui.label(f"test: {method}").classes("text-center text-lg")

    # TODO: get og text from babbler module
    iv = input_view.input_view("the quick brown fox jumps over the lazy dog").classes("w-full")

    input_method = input_method_def()

    def on_text_update(txt: str) -> None:
        iv.set_text(txt)
        state.text = txt

    input_method.on_text_update(on_text_update)
