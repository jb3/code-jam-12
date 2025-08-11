from nicegui import ui


import audio_style_input as _  # noqa: F401
# We probably want to figure out a more clean way to do this without the noqa.
import rpg_text_input as _  # noqa: F401 Importing creates the subpage.


ui.label("Hello NiceGUI!")


@ui.page("/")
def main_page() -> None:
    """Render the main page."""
    with (
        ui.card().classes("w-[100vw] h-[50vh] flex justify-center items-center bg-sky-950"),
        ui.card().classes("no-shadow justify-center items-center"),
    ):
        ui.label("Terrible Typing").classes("text-[48px]")
        ui.label("Test Your Typing Skills").classes("text-[20px]")
        ui.button("Go to Audio Editor", on_click=lambda: ui.navigate.to("/audio_editor"))


ui.run()
