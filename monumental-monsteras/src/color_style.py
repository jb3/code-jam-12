from dataclasses import dataclass


@dataclass
class ColorStyle:
    """The color theme for the website.

    Attributes:
        primary (str): Primary color.
        secondary (str): Secondary color.
        primary_bg (str): Primary background color.
        secondary_bg (str): Secondary background color.
        contrast (str): Color that contrasts with the background color.

    """

    def __init__(self) -> None:
        self.primary: str = "#12E7B2"
        self.secondary: str = "#7D53DE"
        self.primary_bg: str = "#111111"
        self.secondary_bg: str = "#1B1B1B"
        self.contrast: str = "#E9E9E9"
