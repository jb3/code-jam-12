import asyncio
import string
from pathlib import Path
from typing import override

from nicegui import app, ui

import config
from input_method_proto import IInputMethod, TextUpdateCallback

media = Path("./static")
app.add_media_files("/media", media)

char_selection = [string.ascii_uppercase, string.ascii_lowercase, string.punctuation]


class AudioEditorComponent(IInputMethod):
    """Render the audio editor page with spinning record and letter spinner."""

    def __init__(self) -> None:
        self._text_update_callback: TextUpdateCallback | None = None
        self.current_char_selection_index_container = [0]
        self.current_chars_selected = char_selection[0]
        self.current_letter_index_container = [0]
        self.play_pause_toggle = [False]
        self.rotation_container = [0]
        self.normal_spin_speed = 5
        self.boosted_spin_speed = 10
        self.spin_speed_container = [self.normal_spin_speed]
        self.spin_direction_container = [1]
        self.user_text_container = ""

        self.timer_task = None
        self.spin_task = None

        self.intro_card, self.start_button = self.create_intro_card()
        self.main_content, self.record, self.label, self.buttons_row, self.buttons_row_2 = self.create_main_content()

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
        intro_card = ui.card().classes(
            f"w-full h-full flex justify-center items-center bg-[{config.COLOR_STYLE['secondary_bg']}]"
        )
        with intro_card, ui.card().classes("no-shadow justify-center items-center"):
            ui.label("WPM Battle: DJ Edition").classes("text-5xl font-bold")
            ui.label("Use an audio editor to test your typing skills").classes("text-xl")
            start_button = ui.button("Get started!", color=config.COLOR_STYLE["primary"])
        return intro_card, start_button

    def create_main_content(self) -> tuple[ui.column, ui.image, ui.chip, ui.row, ui.row]:
        """Create main content with record image, letter label, and button row.

        Returns:
            tuple: (main_content container, record image, label, buttons row)

        """
        main_content = ui.column().classes("w-full h-full items-center gap-4 #2b87d1").style("display:none")
        with (
            main_content,
            ui.card().classes(
                f"gap-4 w-full h-full flex flex-col justify-center items-center "
                f"bg-[{config.COLOR_STYLE['secondary_bg']}] px-16"
            ),
            ui.element("div").classes("flex flex-row w-full justify-between"),
        ):
            with ui.element("div").classes("flex flex-col w-1/2 h-full justify-center items-center gap-4"):
                chip = ui.chip(text="Current letter: A", color=f"{config.COLOR_STYLE['contrast']}").classes(
                    "relative text-2xl top-[-100px]"
                )
                buttons_row = ui.row().style("gap: 10px")
                buttons_row_2 = ui.row().style("gap: 10x")

            with ui.element("div").classes("flex flex-col w-1/2 h-full justify-center items-center gap-4"):
                record = (
                    ui.image(
                        "/media/images/record.png",
                    )
                    .style("transition: transform 0.05s linear;")
                    .classes("w-1/2")
                )

        return main_content, record, chip, buttons_row, buttons_row_2

    def cycle_char_select(self) -> None:
        """Select character set from Capital, Lower, and Special characters."""
        self.current_char_selection_index_container[0] = (self.current_char_selection_index_container[0] + 1) % len(
            char_selection,
        )
        self.current_chars_selected = char_selection[self.current_char_selection_index_container[0]]
        self.current_letter_index_container[0] = (self.current_letter_index_container[0] + 1) % len(
            self.current_chars_selected,
        )

    async def spin_continuous(self) -> None:
        """Continuously rotate the record image based on spin speed and direction."""
        while True:
            self.rotation_container[0] += self.spin_direction_container[0] * self.spin_speed_container[0]
            self.record.style(f"transform: rotate({self.rotation_container[0]}deg);")
            await asyncio.sleep(0.05)

    async def letter_spinner_task(self) -> None:
        """Continuously update the label with the current letter, cycling through letters."""
        while True:
            self.label.set_text(
                f"Current letter: {self.current_chars_selected[self.current_letter_index_container[0]]}",
            )
            self.current_letter_index_container[0] = (self.current_letter_index_container[0] + 1) % len(
                self.current_chars_selected,
            )
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

    def toggle_play_pause(self) -> None:
        """Toggle play_pause state."""
        self.play_pause_toggle[0] = not self.play_pause_toggle[0]
        self.play_pause_handler()

    def play_pause_handler(self) -> None:
        """Play and puase the letter spinner and spinning."""
        toggle = self.play_pause_toggle[0]

        if toggle:
            self.main_track.play()
            self.on_play()
        else:
            self.main_track.pause()
            self.on_pause()

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
        self.current_letter_index_container[0] = (self.current_letter_index_container[0] + 3) % len(
            self.current_chars_selected,
        )
        self.play_fast_forward_sound()
        self.start_spinning(clockwise=True)
        self._forward_3_task = asyncio.create_task(self.speed_boost(final_direction=1))

    def rewind_3(self) -> None:
        """Skip backward 3 letters with sound and speed boost."""
        self.current_letter_index_container[0] = (self.current_letter_index_container[0] - 3) % len(
            self.current_chars_selected,
        )
        self.play_rewind_sound()
        self.start_spinning(clockwise=False)
        self._speed_boost_task = asyncio.create_task(self.speed_boost(final_direction=1))

    def setup_buttons(self) -> None:
        """Create UI buttons with their event handlers."""
        with self.buttons_row, ui.button_group().classes("gap-1"):
            ui.button("Rewind 3 Seconds", color="#d18b2b", icon="fast_rewind", on_click=self.rewind_3)
            ui.button("Forward 3 Seconds", color="#d18b2b", icon="fast_forward", on_click=self.forward_3)
            ui.button("Next Set of Chars", icon="skip_next", on_click=self.cycle_char_select)
        with self.buttons_row_2, ui.button_group().classes("gap-1"):
            ui.button(
                "Play/Pause",
                color="#2bd157",
                icon="not_started",
                on_click=lambda: [self.toggle_play_pause()],
            )
            ui.button("Eject", color="#d18b2b", icon="eject", on_click=self._delete_letter_handler)
            ui.button("Record", color="red", icon="radio_button_checked", on_click=self._select_letter_handler)
            ui.button("Mute", color="grey", icon="do_not_disturb", on_click=self._add_space_handler)

    def _select_letter_handler(self) -> None:
        """Notify selected letter and trigger text update callback."""
        char = self.current_chars_selected[self.current_letter_index_container[0] - 1]
        ui.notify(f"You selected: {char}")
        self.select_char(char)

    def start_audio_editor(self) -> None:
        """Hide intro card and show main content."""
        self.intro_card.style("display:none")
        self.main_content.style("display:flex")

    @override
    def on_text_update(self, callback: TextUpdateCallback) -> None:
        """Register a callback to be called whenever the text updates.

        Args:
            callback (TextUpdateCallback): Function called with updated text.

        """
        self._text_update_callback = callback

    def select_char(self, char: str) -> None:
        """Call the registered callback with the selected letter.

        Args:
            char (str): The letter selected by the user.

        """
        if char != "back_space":
            self.user_text_container += char
        else:
            self.user_text_container = self.user_text_container[:-1]

        if self._text_update_callback:
            self._text_update_callback(self.user_text_container)

    def _delete_letter_handler(self, char: str = "back_space") -> None:
        """Delete the last letter in user string thus far.

        Args:
           char(str): The code to delete last leter (back_space)

        """
        self.select_char(char)

    def _add_space_handler(self, char: str = " ") -> None:
        """Add a space in user string thus far.

        Args:
         char(str): The space characer to add.

        """
        self.select_char(char)
