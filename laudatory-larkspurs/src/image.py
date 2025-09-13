import base64
import io
import pathlib

from PIL import Image, ImageDraw

from gui.components.image_preview import ImagePreview
from utils.color import Color

IMAGES_DIR = pathlib.Path(__file__).parent.resolve() / "images"


class PaintImage:
    """Image for creation of image objects.

    :author: Mira
    """

    def __init__(self, image_preview: ImagePreview) -> None:
        """Create an image object."""
        self.img_name = ""
        self.img = Image.new("RGB", (400, 250), (0, 0, 0))
        self.backupImage = self.img.copy()
        self.undo_available = True
        self.edits = 0
        self.image_preview = image_preview

    def refresh_image(self) -> None:
        """Display edits on screen."""
        self.edits += 1
        self.image_preview.display_image(self.get_js_link())

    def load(self, image_name: str = "default.png") -> int:
        """Load image from images.

        params image_name: name of an image with .ext
        return returns 0 if image has loaded 1 if the image wasn't located
        """
        if (IMAGES_DIR / image_name).exists():
            self.img = Image.open(IMAGES_DIR / image_name, "r").copy()
            self.img_name = image_name
            self.edits = -1
            self.refresh_image()
            return 0
        return 1

    def save(self, img_name: str) -> int:
        """Save image to images/<img_name>.

        returns 0 if image has saved 1 if the image wasn't
        """
        if not img_name:
            print("Can't save an empty image.")
            return 1
        self.img.save(IMAGES_DIR / img_name, format="PNG")
        self.edits = 0
        return 0

    def get_js_link(self) -> str:
        """Return base64 link for an image file.

        return string - image src link
        """
        buf = io.BytesIO()
        self.img.save(buf, format="PNG")
        data = base64.b64encode(buf.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{data}"

    def load_from_image_link(self, js_link: str) -> None:
        """Load image from a base64 image src link (data URL) into self.img.

        js_link: str - base64 data URL like "data:image/png;base64,iVBORw0..."
        """
        header, encoded = js_link.split(",", 1)
        img_data = base64.b64decode(encoded)
        buf = io.BytesIO(img_data)
        self.img = Image.open(buf)
        self.undo_save()
        self.edits = -1
        self.refresh_image()

    def undo(self) -> int:
        """Return 0 if chages undone, otherwise 1."""
        if self.undo_available:
            self.img = self.backup_image
            self.undo_available = False
            self.refresh_image()
            return 0
        return 1

    def undo_save(self) -> None:
        """Save for undo."""
        self.backup_image = self.img.copy()
        self.undo_available = True

    def get_info(self) -> dict[str, tuple[int, int] | str | bool | list | None]:
        """Return image information dictionary.

        return dictionary containing basic information including: size, format, colors
        """
        return {
            "size": self.img.size,
            "format": self.img.format,
            "edits": self.edits,
            "colors": self.img.getcolors(),
        }

    def set_pixel(self, x: int, y: int, color: Color) -> None:
        """Set an image pixel."""
        self.undo_save()

        draw = ImageDraw.Draw(self.img, "RGBA")
        draw.point((x, y), color.rgb)
        self.refresh_image()

    def get_pixel(self, x: int, y: int) -> tuple[int, ...]:
        """Get an image pixel."""
        return self.img.getpixel((x, y))

    def fill_rect(  # noqa: PLR0913
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        fill_color: Color | None = None,
        outline_color: Color | None = None,
        outline_size: int = 0,
    ) -> int:
        """Fill rectangle on an image.

        return 0 on success 1 on fail
        """
        if width <= 0 or height <= 0:
            return 1

        self.undo_save()

        draw = ImageDraw.Draw(self.img, "RGBA")
        draw.rectangle(
            [x, y, x + width - 1, y + height - 1],
            fill=fill_color.rgba if fill_color else None,
            outline=outline_color.rgba if outline_color else None,
            width=outline_size,
        )
        self.refresh_image()
        return 0

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: Color) -> int:
        """Draw a straight line on the image."""
        self.undo_save()

        draw = ImageDraw.Draw(self.img, "RGBA")
        draw.line((x1, y1, x2, y2), fill=color.rgb)
        self.refresh_image()
        return 0

    def draw_circle(  # noqa: PLR0913
        self,
        cx: int,
        cy: int,
        radius: int,
        fill_color: Color | None = None,
        outline_color: Color | None = None,
        outline_size: int = 0,
    ) -> int:
        """Draw a circle on the image."""
        self.undo_save()

        draw = ImageDraw.Draw(self.img, "RGBA")
        bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
        draw.ellipse(
            bbox,
            fill=fill_color.rgba if fill_color else None,
            outline=outline_color.rgba if outline_color else None,
            width=outline_size,
        )
        self.refresh_image()
        return 0

    def draw_polygon(
        self,
        points: list[tuple[int, int]],
        fill_color: Color | None = None,
        outline_color: Color | None = None,
        outline_size: int = 0,
    ) -> int:
        """Fill polygon on an image.

        Return 0 on success 1 on fail
        """
        self.undo_save()

        draw = ImageDraw.Draw(self.img, "RGBA")
        draw.polygon(
            points,
            fill=fill_color.rgba if fill_color else None,
            outline=outline_color.rgba if outline_color else None,
            width=outline_size,
        )
        self.refresh_image()
        return 0
