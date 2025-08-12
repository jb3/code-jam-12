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

        self.main_track = (
            ui.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3")
            .props(remove="controls")
            .props("loop")
        )
        self.rewind_sound = ui.audio("/media/sounds/rewind.mp3").style("display:none")
        self.fast_forward_sound = ui.audio("/media/sounds/fast_forward.mp3").style("display:none")
