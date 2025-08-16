import audio_style_input
import rpg_text_input

PROJECT_NAME: str = "Dynamic Typing"
PROJECT_DESCRIPTION: str = "How fast can you type?"

# INPUT METHODS
INPUT_METHODS: list[dict] = [
    {
        "name": "Record Player",
        "path": "/audio-input",
        "icon": "",
        "component": audio_style_input,
    },
    {
        "name": "WASD",
        "path": "/wasd",
        "icon": "",
        "component": rpg_text_input,
    },
    {
        "name": "Color Picker",
        "path": "/color-picker",
        "icon": "",
        "component": "",
    },
    {
        "name": "Circle Selector",
        "path": "/circle-selector",
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
