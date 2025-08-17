from nicegui import ui

import platformer_input.platformer_constants as c


class PlatformerSceneComponent(ui.element):
    """Displays the characters and scene within the game."""

    mask_element: ui.element
    world: list[list[str]]

    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__("div")

        with self:
            self.mask_element = ui.element("div")
        self.mask_element.style(
            f"width: {c.TILE_SIZE * c.SCENE_WIDTH}px; height: {c.TILE_SIZE * c.SCENE_HEIGHT}px;"
            f"background-color: {c.COLOR_BG}; position: relative; overflow: hidden; border: 2px solid black"
        )

        self.world = c.world_grid()
        self.world_height = len(self.world)

        with self.mask_element:
            self.map_container = ui.element("div")
        self.map_container.style(
            f"position:absolute;width:{len(self.world[0]) * c.TILE_SIZE}px;"
            f"height:{len(self.world) * c.TILE_SIZE}px;"
            f"display:grid;grid-template-columns:repeat({len(self.world[0])}, {c.TILE_SIZE}px);"
            f"grid-template-rows:repeat({len(self.world)}, {c.TILE_SIZE}px);"
        )

        self.px_player_offset_lx = ((c.SCENE_WIDTH - 1) * c.TILE_SIZE) / 2
        self.px_player_offset_ty = (c.SCENE_HEIGHT * c.TILE_SIZE) - 2 * c.TILE_SIZE
        with self.mask_element:
            ui.element("div").style(
                f"position:absolute;top:{self.px_player_offset_ty}px;left:{self.px_player_offset_lx}px;"
                f"background-color:{c.COLOR_PLAYER};width:{c.TILE_SIZE}px;height:{c.TILE_SIZE}px"
            )

        with self.map_container:
            for row in self.world:
                for cell in row:
                    ui.element("div").style(f"background-color:{self._get_bg_color(cell)}")

        self.move_player(*position)

    def move_player(self, player_x: float, player_y: float) -> None:
        """Move the player in the renderer."""
        px_left = self.px_player_offset_lx - player_x * c.TILE_SIZE
        self.map_container.style(f"left:{px_left}px")

        px_top = self.px_player_offset_ty - player_y * c.TILE_SIZE
        self.map_container.style(f"top:{px_top}px")

    def _get_bg_color(self, scp: str) -> str:
        """Get the background color in a tile by the tile type."""
        if scp == "#":
            return c.COLOR_GROUND
        if scp == " ":
            return c.COLOR_BG
        return "red"
