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

        with self.map_container:
            for row in self.world:
                for cell in row:
                    ui.element("div").style(f"background-color:{self._get_bg_color(cell)}")

        self.move_player(*position)

    def move_player(self, player_x: float, player_y: float) -> None:
        """Move the player in the renderer."""
        self.map_container.style(f"right:{player_x * c.TILE_SIZE}px;bottom:{player_y * c.TILE_SIZE}px")

    def _get_bg_color(self, scp: str) -> str:
        """Get the background color in a tile by the tile type."""
        if scp == "#":
            return c.COLOR_GROUND
        if scp == " ":
            return c.COLOR_BG
        return "red"
