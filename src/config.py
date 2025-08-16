from audio_style_input import AudioEditorComponent

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
        "component": None,
    },
    {
        "name": "Color Picker",
        "path": "color-picker",
        "icon": "",
        "component": None,
    },
    {
        "name": "Circle Selector",
        "path": "circle-selector",
        "icon": "",
        "component": None,
    },
]

# COLORS
COLOR_STYLE: dict = {
    "PRIMARY": "",
    "SECONDARY": "",
    "PRIMARY_BG": "",
    "SECONDARY_BG": "",
}
