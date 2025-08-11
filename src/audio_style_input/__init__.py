from pathlib import Path

from nicegui import app, ui

media = Path("./static")
app.add_media_files("/media", media)


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

    main_content = ui.column().classes("items-center gap-4").style("display:none")

    with main_content, ui.card().classes("w-[100vw] h-[50vh] flex justify-center items-center bg-sky-950"):
        ui.image("/media/images/record.png").style("width: 500px;")
        ui.label("Current letter: A")

    def start_audio_editor() -> None:
        """Switch from intro card to main content."""
        intro_card.style("display:none")
        main_content.style("display:flex")

    start_button.on("click", start_audio_editor)


ui.run()
