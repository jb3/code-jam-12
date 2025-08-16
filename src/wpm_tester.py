from dataclasses import dataclass

from nicegui import ui

import input_method_proto
import input_view
from config import INPUT_METHODS


def get_input_method_by_name(inmth: str) -> type[input_method_proto.IInputMethod] | None:
    """Get an input method class by it's name.

    :returns: `type[IInputMethod]` on success, `None` on failure.
    """
    for input_method in INPUT_METHODS:
        if inmth == input_method["path"]:
            return input_method["component"]
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
    timer_on = False
    timer_container = None

    input_method_def = get_input_method_by_name(method)
    if input_method_def is None:
        ui.navigate.to("/")
        return

    with ui.header(elevated=True).classes("align-center justify-center"):
        ui.label(f"test: {method}").classes("text-center text-lg")

    # TODO: get og text from babbler module
    iv = input_view.input_view("the quick brown fox jumps over the lazy dog").classes("w-full")

    timer_label = ui.label()

    input_method = input_method_def()

    def on_text_update(txt: str) -> None:
        nonlocal timer_on, timer_container
        if not timer_on:
            timer_container = ui.timer(1, lambda: timer_label.set_text(iv.update_timer()))
            timer_on = True
        iv.set_text(txt)
        state.text = txt

    def stop_timer() -> None:
        nonlocal timer_container
        if timer_container:
            timer_container.deactivate()

    input_method.on_text_update(on_text_update)

    ui.on("disconnect", stop_timer)
