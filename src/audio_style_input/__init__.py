from nicegui import ui


@ui.page("/audio_editor")
def audio_editor_page() -> None:
    """Render the audio editor intro page."""
    with (
        ui.card().classes("w-[100vw] h-[50vh] flex justify-center items-center bg-sky-950") as intro_card,
        ui.card().classes("no-shadow justify-center items-center"),
    ):
        ui.label("WPM Battle: DJ Edition").classes("text-[48px]")
        ui.label("Use an audio editor to test your typing skills").classes("text-[20px]")
        start_button = ui.button("Get started!")

    def start_audio_editor() -> None:
        """Hide the intro card."""
        intro_card.style("display:none")

    start_button.on("click", start_audio_editor)


ui.run()
