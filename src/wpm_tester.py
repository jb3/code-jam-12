import time
from dataclasses import dataclass

from nicegui import ui

import input_method_proto
import input_view
from config import COLOR_STYLE, INPUT_METHODS, PROJECT_NAME


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

    ui.add_css("""
        .header {
            height: 8vh;
            align-items: center;
        }
        .h1 {
            font-family: Arial;
            font-size: 35px;
            font-weight: bold;
        }
        .input-method-container {
            display: flex;
            flex-direction: column;
            justify-content: space-evenly;
            position: absolute;
            width: 90vw;
            height: 85vh;
            left: 50%;
            top: 50%;
            transform: translate(-50%, -50%);
            border-radius: 20px
        }
        body {
            margin: 0;
            padding: 0;
            height: 100%;
            width: 100%;
        }
    """)

    # Header
    with (
        ui.header(wrap=False)
        .style(f"background-color: {COLOR_STYLE['secondary_bg']}")
        .classes("items-center justify-between header")
    ):
        with ui.card().props("flat"):  # small logo placeholder
            pass
        ui.label(PROJECT_NAME.upper()).style(f"color: {COLOR_STYLE['primary']}").classes("h1")
        ui.button(on_click=lambda: right_drawer.toggle(), icon="menu").props("flat color=white")

    # Sidebar
    with (
        ui.right_drawer(
            value=False,
            fixed=False,
        )
        .style(f"background-color: {COLOR_STYLE['secondary_bg']}")
        .props("overlay")
        .classes("p-0") as right_drawer,
        ui.element("q-scroll-area").classes("fit"),
    ):
        # Home Button
        with (
            ui.list().classes("fit"),
            ui.item(on_click=lambda: ui.navigate.to("/"))
            .props("clickable")
            .classes(f"hover:bg-[{COLOR_STYLE['primary']}]"),
            ui.item_section(),
        ):
            ui.label("HOME").style(f"color: {COLOR_STYLE['contrast']}")

        with ui.list().classes("fit"), ui.column().classes("w-full items-center"):
            ui.separator().style("background-color: #313131; width: 95%;")

        # Input method buttons
        with ui.list().classes("fit"):
            for input in INPUT_METHODS:
                with (
                    ui.item(on_click=lambda _, path=f"/test/{input['path']}": ui.navigate.to(path))
                    .props("clickable")
                    .classes(f"hover:bg-[{COLOR_STYLE['primary']}]"),
                    ui.item_section(),
                ):
                    ui.label(input["name"].upper()).style(f"color: {COLOR_STYLE['contrast']}")

    # Main body
    ui.query("body").style(f"background-color: {COLOR_STYLE['primary_bg']};")

    with (
        ui.element("div")
        .style(f"background-color: {COLOR_STYLE['secondary_bg']}")
        .classes("input-method-container items-center")
    ):
        # Sentence & timer div
        with ui.element("div"):
            # TODO: get og text from babbler module
            iv = input_view.input_view("the quick brown fox jumps over the lazy dog").classes("w-full")
            with ui.row().classes("w-full justify-center items-center gap-4"):
                timer_label = ui.chip("TIMER: 0:00", color="#6AC251", icon="timer")
                wpm_label = ui.chip("WPM: --", color="#e5e5e5", icon="watch")
                wph_label = ui.chip("WPH: --", color="#e5e5e5", icon="hourglass_top")

        # Input method div
        with ui.element("div"):
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
