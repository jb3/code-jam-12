<!-- color_formats.md -->

# Color Formats

These color formats are accepted by commands that take a `<color>` argument (e.g. `bg`, `fg`, `draw_*`, `terminal_background`, etc.).

## Supported Formats

- Space- or comma-separated `R G B [A]` (0–255)
- Hex `#RRGGBB`
- Named CSS colors
  - List can be found [here](https://developer.mozilla.org/en-US/docs/Web/CSS/named-color)
- Functional notations:
  - `rgb(r g b)` / `rgb(r, g, b)`
  - `rgba(r g b a)` / `rgba(r, g, b, a)`
  - `hsv(h s v)` / `hsva(h s v a)`

## Examples

- `255 255 255`
- `100,0,0,255`
- `gold`
- `#C0FFEE`
- `rgb(0 200 150)`
- `rgba(0 255 255 100)`
- `hsv(360 100 100)`

> Alpha channel (A) is optional. Values are rejected if out of bounds.
