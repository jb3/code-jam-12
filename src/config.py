from audio_style_input import AudioEditorComponent
from rpg_text_input import rpg_text_input_page

PROJECT_NAME: str = "Dynamic Typing"
PROJECT_DESCRIPTION: str = "How fast can you type?"

# INPUT METHODS
INPUT_METHODS: list[dict] = [
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
        "component": rpg_text_input_page,
    },
    {
        "name": "Color Picker",
        "path": "color-picker",
        "icon": "",
        "component": "",
    },
    {
        "name": "Circle Selector",
        "path": "circle-selector",
        "icon": "",
        "component": "",
    },
]

# COLORS
COLOR_STYLE: dict = {
    "PRIMARY": "",
    "SECONDARY": "",
    "PRIMARY_BG": "",
    "SECONDARY_BG": "",
}
