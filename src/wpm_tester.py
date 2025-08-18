import secrets
import time
from dataclasses import dataclass

from faker import Faker
from nicegui import ui

import input_method_proto
import input_view
from config import COLOR_STYLE, INPUT_METHODS, PROJECT_NAME

fake = Faker()


def get_input_method_by_name(inmth: str) -> type[input_method_proto.IInputMethod] | None:
    """Get an input method class by its name."""
    for input_method in INPUT_METHODS:
        if inmth == input_method["path"]:
            return input_method["component"]
    return None


@dataclass
class TimerState:
    """Timer state class."""

    active: bool = False
    container: ui.timer | None = None
    start: float | None = None


@dataclass
class WpmTesterPageState:
    """The page state."""

    """Useless for now, may be useful later?"""
    text: str


def create_header() -> None:
    """Create header and sidebar."""
    # Header
    with (
        ui.header(wrap=False)
        .style(f"background-color: {COLOR_STYLE['secondary_bg']}")
        .classes("flex items-center justify-between h-[8vh] py-0 px-4")
    ):
        with ui.card().props("flat"):  # small logo placeholder
            pass
        (
            ui.label(PROJECT_NAME.upper())
            .style(f"color: {COLOR_STYLE['primary']}; font-family: Arial, sans-serif;")
            .classes("text-4xl font-bold")
        )
        ui.button(on_click=lambda: right_drawer.toggle(), icon="menu").props("flat color=white")

    # Sidebar
    with (
        ui.right_drawer(value=False, fixed=False)
        .style(f"background-color: {COLOR_STYLE['secondary_bg']}")
        .props("overlay")
        .classes("p-0") as right_drawer,
        ui.element("q-scroll-area").classes("fit"),
    ):
        # Home nav button
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

        # Input method nav buttons
        with ui.list().classes("fit"):
            for input_method in INPUT_METHODS:
                path = f"/test/{input_method['path']}"
                with (
                    ui.item(on_click=lambda _, p=path: ui.navigate.to(p))
                    .props("clickable")
                    .classes(f"hover:bg-[{COLOR_STYLE['primary']}]"),
                    ui.item_section(),
                ):
                    ui.label(input_method["name"].upper()).style(f"color: {COLOR_STYLE['contrast']}")


def create_time_chips() -> tuple[ui.chip, ui.chip, ui.chip]:
    """Create chips for timer, wpm, and wph."""
    with ui.row().classes("w-full justify-center items-center gap-4"):
        timer_label = ui.chip("TIMER: 0:00", color="#6AC251", icon="timer")
        wpm_label = ui.chip("WPM: --", color="#e5e5e5", icon="watch")
        wph_label = ui.chip("WPH: --", color="#e5e5e5", icon="hourglass_top")

    return timer_label, wpm_label, wph_label


def setup(
    method: str,
    text_to_use: str,
    state: WpmTesterPageState,
    chip_package: tuple[ui.chip, ui.chip, ui.chip],
    iv: input_view.input_view,
) -> None:
    """Set up input method updates and timer handling."""
    input_method_def = get_input_method_by_name(method)
    if input_method_def is None:
        return

    input_method = input_method_def()
    timer = TimerState()
    timer_label, wpm_label, wph_label = chip_package

    def stop_timer() -> None:
        if timer.container:
            timer.container.deactivate()

    def on_text_update(txt: str) -> None:
        if not timer.active:
            timer.container = ui.timer(1, lambda: timer_label.set_text(iv.update_timer()))
            timer.active = True
            timer.start = time.time()

        iv.set_text(txt)
        state.text = txt

        if len(txt) == len(text_to_use):
            elapsed = time.time() - timer.start if timer.start else 0
            if elapsed > 0:
                wpm = (len(txt) / 5) / (elapsed / 60)
                wpm_label.set_text(f"Finished! WPM: {int(wpm)}")
                wph_label.set_text(f"Finished! WPH: {int(wpm * 60)}")
            stop_timer()

    input_method.on_text_update(on_text_update)
    ui.on("disconnect", stop_timer)


def create_sentence() -> str:
    """Create sentence to use in challenge."""
    punctuation = [".", "!"]
    sentence = fake.sentence(nb_words=6, variable_nb_words=False)
    return sentence[:-1] + secrets.choice(punctuation)


async def wpm_tester_page(method: str) -> None:
    """Create the WPM tester page for a given input method."""
    input_method_def = get_input_method_by_name(method)
    if input_method_def is None:
        ui.navigate.to("/")
        return

    state = WpmTesterPageState("")
    text_to_use = create_sentence()

    create_header()

    # Main body
    ui.query("body").style(f"background-color: {COLOR_STYLE['primary_bg']};")

    with (
        ui.element("div")
        .style(f"background-color: {COLOR_STYLE['secondary_bg']}")
        .classes(
            """flex flex-col justify-evenly items-center absolute w-[90vw] h-[85vh] left-1/2 top-1/2
             transform -translate-x-1/2 -translate-y-1/2 rounded-xl"""
        )
    ):
        # Sentence and timer div
        with ui.element("div").classes("flex items-center w-full h-1/4 p-5"):
            iv = input_view.input_view(text_to_use).classes("w-full")
            chip_package = create_time_chips()

        # Input method div
        with ui.element("div").classes("align-items w-full h-3/4"):
            setup(method, text_to_use, state, chip_package, iv)
