from commands.background import Background
from commands.base_command import BaseCommand
from commands.draw_circle import DrawCircle
from commands.draw_line import DrawLine
from commands.draw_pixel import DrawPixel
from commands.draw_polygon import DrawPolygon
from commands.draw_rectangle import DrawRectangle
from commands.foreground import Foreground
from commands.help import Help
from commands.image_info import ImageInfo
from commands.load_image import LoadImage
from commands.ls import Ls
from commands.ping import Ping
from commands.save_image import SaveImage
from commands.terminal_background import TerminalBackground
from commands.undo import Undo

all_commands: dict[str, BaseCommand] = {
    Ls.name: Ls(),
    Help.name: Help(),
    Ping.name: Ping(),
    Undo.name: Undo(),
    DrawLine.name: DrawLine(),
    DrawPixel.name: DrawPixel(),
    ImageInfo.name: ImageInfo(),
    LoadImage.name: LoadImage(),
    SaveImage.name: SaveImage(),
    TerminalBackground.name: TerminalBackground(),
    DrawCircle.name: DrawCircle(),
    DrawRectangle.name: DrawRectangle(),
    Foreground.name: Foreground(),
    Background.name: Background(),
    DrawPolygon.name: DrawPolygon(),
}
