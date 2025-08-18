from typing import TypedDict

from audio_style_input import AudioEditorComponent
from color_mixer_input import ColorInputComponent
from input_method_proto import IInputMethod
from platformer_input import PlatformerInputMethod
from rpg_text_input import Keyboard

PROJECT_NAME: str = "Dynamic Typing"
PROJECT_DESCRIPTION: str = "How fast can you type?"


class InputMethodSpec(TypedDict):
    """Specifications for an input method to be added to the main page."""

    name: str
    path: str
    icon: str
    component: type[IInputMethod] | None


# INPUT METHODS
INPUT_METHODS: list[InputMethodSpec] = [
    {
        "name": "Record Player",
        "path": "audio-input",
        "icon": "",
        "component": AudioEditorComponent,
    },
    {
        "name": "WASD",
        "path": "wasd",
        "icon": "",
        "component": Keyboard,
    },
    {
        "name": "Color Picker",
        "path": "color-picker",
        "icon": "",
        "component": ColorInputComponent,
    },
    {
        "name": "Platformer",
        "path": "platformer",
        "icon": "",
        "component": PlatformerInputMethod,
    },
]
