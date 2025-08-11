from nicegui import ui

import audio_style_input as _  # noqa: F401

ui.label("Hello NiceGUI!")


@ui.page("/")
def main_page() -> None:
    """Render the main page."""
    with (
        ui.card().classes("w-[100vw] h-[50vh] flex justify-center items-center bg-sky-950"),
        ui.card().classes("no-shadow justify-center items-center"),
    ):
        ui.label("Audio Editor Of The Future").classes("text-[48px]")
        ui.label("Use an audio editor to test your typing skills").classes("text-[20px]")
        ui.button("Go to Audio Editor", on_click=lambda: ui.navigate.to("/audio_editor"))


ui.run()
