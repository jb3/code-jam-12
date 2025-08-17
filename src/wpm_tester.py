import time
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
    start_time = None

    input_method_def = get_input_method_by_name(method)
    if input_method_def is None:
        ui.navigate.to("/")
        return

    with ui.header(elevated=True).classes("align-center justify-center"):
        ui.label(f"test: {method}").classes("text-center text-lg")

    # TODO: get og text from babbler module
    text_to_use = "the quick brown fox jumps over the lazy dog"
    iv = input_view.input_view(text_to_use).classes("w-full")
    with ui.row().classes("w-full justify-center items-center gap-4"):
        timer_label = ui.chip("TIMER: 0:00", color="#6AC251", icon="timer")
        wpm_label = ui.chip("WPM: --", color="#e5e5e5", icon="watch")
        wph_label = ui.chip("WPH: --", color="#e5e5e5", icon="hourglass_top")

    input_method = input_method_def()

    def on_text_update(txt: str) -> None:
        nonlocal timer_on, timer_container, text_to_use, start_time
        if not timer_on:
            timer_container = ui.timer(1, lambda: timer_label.set_text(iv.update_timer()))
            timer_on = True
            start_time = time.time()
        iv.set_text(txt)
        state.text = txt

        if len(txt) == len(text_to_use):
            elapsed_seconds = time.time() - start_time
            if elapsed_seconds > 0:
                chars_typed = len(txt)
                wpm = (chars_typed / 5) / (elapsed_seconds / 60)
                wpm_label.set_text(f"Finished! WPM: {int(wpm)}")
                wph_label.set_text(f"Finished! WPH: {int(wpm * 60)}")
            stop_timer()

    def stop_timer() -> None:
        nonlocal timer_container
        if timer_container:
            timer_container.deactivate()

    input_method.on_text_update(on_text_update)

    ui.on("disconnect", stop_timer)
