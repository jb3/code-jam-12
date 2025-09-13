import re
from colorsys import hsv_to_rgb
from dataclasses import dataclass
from math import atan2, degrees, sqrt

import webcolors


@dataclass
class Color:
    """Color class.

    Has various conversion and output methods.
    """

    r: int
    g: int
    b: int
    a: int = 255

    @property
    def rgb(self) -> tuple[int, int, int]:
        """Output as RGB tuple."""
        return self.r, self.g, self.b

    @property
    def rgba(self) -> tuple[int, int, int, int]:
        """Output as RGBA tuple."""
        return self.r, self.g, self.b, self.a

    @property
    def hex(self) -> str:
        """Output as hexadecimal string."""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}{self.a:02x}"

    @property
    def hsv(self) -> tuple[float, float, float]:
        """Output as tuple in HSV color space."""
        mx = max(self.r, self.g, self.b)
        mn = min(self.r, self.g, self.b)
        df = mx - mn
        h = 0
        if mx == mn:
            h = 0
        elif mx == self.r:
            h = (60 * ((self.g - self.b) / df) + 360) % 360
        elif mx == self.g:
            h = (60 * ((self.b - self.r) / df) + 120) % 360
        elif mx == self.b:
            h = (60 * ((self.r - self.g) / df) + 240) % 360
        s = 0 if mx == 0 else df / mx
        v = mx
        return h, s * 100, v / 255

    @property
    def xyz(self) -> tuple[float, float, float]:
        """Output as tuple in XYZ color space."""
        r, g, b = (self.r / 255.0, self.g / 255.0, self.b / 255.0)
        r = r / 12.92 if r <= 0.04045 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.04045 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.04045 else ((b + 0.055) / 1.055) ** 2.4
        r, g, b = r * 100, g * 100, b * 100
        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505
        return x, y, z

    @property
    def lab(self) -> tuple[float, float, float]:
        """Output as tuple in LAB color space."""
        x, y, z = [value / ref for value, ref in zip(self.xyz, (95.047, 100.000, 108.883), strict=False)]
        x = x ** (1 / 3) if x > 0.008856 else (7.787 * x) + (16 / 116)
        y = y ** (1 / 3) if y > 0.008856 else (7.787 * y) + (16 / 116)
        z = z ** (1 / 3) if z > 0.008856 else (7.787 * z) + (16 / 116)
        l = (116 * y) - 16
        a = 500 * (x - y)
        b = 200 * (y - z)
        return l, a, b

    @property
    def lch(self) -> tuple[float, float, float]:
        """Output as tuple in LCH color space."""
        l, a, b = self.lab
        c = sqrt(a**2 + b**2)
        h = degrees(atan2(b, a))
        h = h + 360 if h < 0 else h
        return l, c, h


def create_color(color_string: str) -> Color:
    """Create a color object from string.

    This string can be hex, name of color or rgb integers separated by comma or space

    @author Philip
    """
    try:
        return Color(*webcolors.hex_to_rgb(color_string))
    except ValueError:
        pass
    try:
        return Color(*webcolors.name_to_rgb(color_string))
    except ValueError:
        pass

    color_string = color_string.lower()

    sep = r"(?:, |,| )"
    match = re.search(rf"^(\d+){sep}(\d+){sep}(\d+)(?:{sep}(\d+))?$", color_string) or re.search(
        rf"^rgba?\((\d+){sep}(\d+){sep}(\d+)(?:{sep}(\d+))?\)$",
        color_string,
    )
    if match:
        return rgb_factory(*(int(i) for i in match.groups() if i is not None))

    match = re.search(rf"^hsva?\((\d+){sep}(\d+){sep}(\d+)(?:{sep}(\d+))?\)$", color_string)
    if match:
        return hsv_factory(*(int(i) for i in match.groups() if i is not None))

    msg = f"Invalid color: {color_string}"
    raise ValueError(msg)


def rgb_factory(r: int, g: int, b: int, a: int | None = None) -> Color:
    """Create Color from rgb values with checks."""
    if r < 0 or r > 255:
        msg = f"r must be between 0 and 255: {r}"
        raise ValueError(msg)

    if g < 0 or g > 255:
        msg = f"g must be between 0 and 255: {g}"
        raise ValueError(msg)

    if b < 0 or b > 255:
        msg = f"b must be between 0 and 255: {b}"
        raise ValueError(msg)

    if a and (a < 0 or a > 255):
        msg = f"a must be between 0 and 255: {a}"
        raise ValueError(msg)

    return Color(r, g, b, a if a else 255)


def hsv_factory(h: int, s: int, v: int, a: int | None = None) -> Color:
    """Create Color from hsv values with checks."""
    if h < 0 or h > 360:
        msg = f"h must be between 0 and 360: {h}"
        raise ValueError(msg)
    h /= 360

    if s < 0 or s > 100:
        msg = f"s must be between 0 and 100: {s}"
        raise ValueError(msg)
    s /= 100

    if v < 0 or v > 100:
        msg = f"v must be between 0 and 100: {v}"
        raise ValueError(msg)
    v /= 100

    if a and (a < 0 or a > 255):
        msg = f"a must be between 0 and 255: {a}"
        raise ValueError(msg)

    r, g, b = hsv_to_rgb(h, s, v)
    r *= 255
    g *= 255
    b *= 255

    return Color(int(r), int(g), int(b), a if a else 255)


colors = {
    "black": Color(0, 0, 0),
    "white": Color(255, 255, 255),
    "red": Color(255, 0, 0),
    "green": Color(0, 255, 0),
    "blue": Color(0, 0, 255),
    "yellow": Color(255, 255, 0),
    "cyan": Color(0, 255, 255),
    "magenta": Color(255, 0, 255),
    "gray": Color(128, 128, 128),
    "maroon": Color(128, 0, 0),
    "olive": Color(128, 128, 0),
    "purple": Color(128, 0, 128),
    "teal": Color(0, 128, 128),
    "navy": Color(0, 0, 128),
    "silver": Color(192, 192, 192),
    "lime": Color(0, 255, 0),
    "orange": Color(255, 165, 0),
    "brown": Color(165, 42, 42),
    "pink": Color(255, 192, 203),
    "gold": Color(255, 215, 0),
}
