import asyncio
from collections.abc import Callable
from pathlib import Path

from nicegui import app, ui

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

    async def spin_continuous(self) -> None:
        """Continuously rotate the record image based on spin speed and direction."""
        while True:
            self.rotation_container[0] += self.spin_direction_container[0] * self.spin_speed_container[0]
            self.record.style(f"transform: rotate({self.rotation_container[0]}deg);")
            await asyncio.sleep(0.05)

    async def letter_spinner_task(self) -> None:
        """Continuously update the label with the current letter, cycling through letters."""
        while True:
            self.label.set_text(f"Current letter: {letters[self.current_letter_index_container[0]]}")
            self.current_letter_index_container[0] = (self.current_letter_index_container[0] + 1) % len(letters)
            await asyncio.sleep(0.5)

    def start_spinning(self, *, clockwise: bool = True) -> None:
        """Start spinning the record image.

        Args:
            clockwise (bool): Direction of spin; True for clockwise, False for counterclockwise.

        """
        self.spin_direction_container[0] = 1 if clockwise else -1
        if self.spin_task is None or self.spin_task.done():
            self.spin_task = asyncio.create_task(self.spin_continuous())

    def stop_spinning(self) -> None:
        """Stop spinning the record image."""
        if self.spin_task:
            self.spin_task.cancel()

    async def speed_boost(self, final_direction: int = 1) -> None:
        """Temporarily increase spin speed and then restore it.

        Args:
            final_direction (int): Direction to set after boost (1 or -1).

        """
        self.spin_speed_container[0] = self.boosted_spin_speed
        await asyncio.sleep(1)
        self.spin_speed_container[0] = self.normal_spin_speed
        self.spin_direction_container[0] = final_direction

    def on_play(self) -> None:
        """Start letter spinner and spinning."""
        if self.timer_task is None or self.timer_task.done():
            self.timer_task = asyncio.create_task(self.letter_spinner_task())
        self.start_spinning(clockwise=True)

    def on_pause(self) -> None:
        """Stop letter spinner and spinning."""
        if self.timer_task:
            self.timer_task.cancel()
        self.stop_spinning()

    def play_rewind_sound(self) -> None:
        """Play rewind sound effect."""
        self.rewind_sound.play()

    def play_fast_forward_sound(self) -> None:
        """Play fast forward sound effect."""
        self.fast_forward_sound.play()

    def forward_3(self) -> None:
        """Skip forward 3 letters with sound and speed boost."""
        self.current_letter_index_container[0] = (self.current_letter_index_container[0] + 3) % len(letters)
        self.play_fast_forward_sound()
        self.start_spinning(clockwise=True)
        self._forward_3_task = asyncio.create_task(self.speed_boost(final_direction=1))

    def rewind_3(self) -> None:
        """Skip backward 3 letters with sound and speed boost."""
        self.current_letter_index_container[0] = (self.current_letter_index_container[0] - 3) % len(letters)
        self.play_rewind_sound()
        self.start_spinning(clockwise=False)
        self._speed_boost_task = asyncio.create_task(self.speed_boost(final_direction=1))

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

    def _select_letter_handler(self) -> None:
        """Notify selected letter and trigger text update callback."""
        letter = letters[self.current_letter_index_container[0] - 1]
        ui.notify(f"You selected: {letter}")
        self.select_letter(letter)

    def start_audio_editor(self) -> None:
        """Hide intro card and show main content."""
        self.intro_card.style("display:none")
        self.main_content.style("display:flex")

    def on_text_update(self, callback: Callable[[str], None]) -> None:
        """Register a callback to be called whenever the text updates.

        Args:
            callback (Callable[[str], None]): Function called with updated text.

        """
        self._text_update_callback = callback

    def select_letter(self, letter: str) -> None:
        """Call the registered callback with the selected letter.

        Args:
            letter (str): The letter selected by the user.

        """
        if self._text_update_callback:
            self._text_update_callback(letter)
