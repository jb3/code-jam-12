from pathlib import Path
from typing import TYPE_CHECKING

from nicegui import app, ui

if TYPE_CHECKING:
    from collections.abc import Callable


import input_method_proto

media = Path("./static")
app.add_media_files("/media", media)

letters = [chr(i) for i in range(ord("A"), ord("Z") + 1)]


class AudioEditorComponent(input_method_proto.IInputMethod):
    """Render the audio editor page with spinning record and letter spinner."""

    def __init__(self) -> None:
        self._text_update_callback: Callable[[str], None] | None = None
        self.current_letter_index_container = [0]
        self.rotation_container = [0]
        self.normal_spin_speed = 5
        self.boosted_spin_speed = 10
        self.spin_speed_container = [self.normal_spin_speed]
        self.spin_direction_container = [1]

        self.timer_task = None
        self.spin_task = None

        self.intro_card, self.start_button = self.create_intro_card()
        self.main_content, self.record, self.label, self.buttons_row = self.create_main_content()

        self.main_track = (
            ui.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3")
            .props(remove="controls")
            .props("loop")
        )
        self.rewind_sound = ui.audio("/media/sounds/rewind.mp3").style("display:none")
        self.fast_forward_sound = ui.audio("/media/sounds/fast_forward.mp3").style("display:none")

        self.setup_buttons()
        self.start_button.on("click", self.start_audio_editor)

    def create_intro_card(self) -> tuple[ui.card, ui.button]:
        """Create the intro card with title and start button.

        Returns:
            tuple: (intro_card, start_button)

        """
        intro_card = ui.card().classes("w-[100vw] h-[50vh] flex justify-center items-center bg-[#d18b2b]")
        with intro_card, ui.card().classes("no-shadow justify-center items-center"):
            ui.label("WPM Battle: DJ Edition").classes("text-[86px]")
            ui.label("Use an audio editor to test your typing skills").classes("text-[28px]")
            start_button = ui.button("Get started!", color="#ff9900")
        return intro_card, start_button

    def create_main_content(self) -> tuple[ui.column, ui.image, ui.label, ui.row]:
        """Create main content with record image, letter label, and button row.

        Returns:
            tuple: (main_content container, record image, label, buttons row)

        """
        main_content = ui.column().classes("items-center gap-4 #2b87d1").style("display:none")
        with (
            main_content,
            ui.card().classes(
                "gap-8 w-[100vw] h-[50vh] flex flex-col justify-center items-center bg-[#2b87d1]",
            ),
        ):
            record = ui.image(
                "/media/images/record.png",
            ).style("width: 300px; transition: transform 0.05s linear;")
            label = ui.label("Current letter: A")
            buttons_row = ui.row().style("gap: 10px")
        return main_content, record, label, buttons_row

    def setup_buttons(self) -> None:
        """Create UI buttons with their event handlers."""
        with self.buttons_row:
            ui.button("Play", color="#d18b2b", on_click=lambda: [self.main_track.play(), self.on_play()])
            ui.button("Pause", color="#d18b2b", on_click=lambda: [self.main_track.pause(), self.on_pause()])
            ui.button("Rewind 3 Seconds", color="#d18b2b", on_click=self.rewind_3)
            ui.button("Forward 3 Seconds", color="#d18b2b", on_click=self.forward_3)
            ui.button(
                "Select Letter",
                color="green",
                on_click=self._select_letter_handler,
            )
