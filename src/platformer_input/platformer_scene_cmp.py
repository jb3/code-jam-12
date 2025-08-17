import math

from nicegui import ui

import platformer_input.platformer_constants as c


class PlatformerSceneComponent(ui.element):
    """Displays the characters and scene within the game."""

    e: ui.element
    world: list[list[str]]

    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__("div")

        self.e = ui.element("div")
        self.e.style(
            f"width: {c.TILE_SIZE * c.SCENE_WIDTH}px; height: {c.TILE_SIZE * c.SCENE_HEIGHT}px;"
            f"background-color: {c.COLOR_BG}; position: relative"
        )

        self.world = c.world_grid()
        self.player_center_x_offset = math.floor((c.SCENE_WIDTH - c.TILE_SIZE_ML) / 2)
        self.player_center_y_offset = c.SCENE_HEIGHT - (2 * c.TILE_SIZE_ML)

        self.draw_scene(*position)

    def draw_scene(self, player_x: int, player_y: int) -> None:
        """Draw the scene, player, etc."""
        self.e.clear()
        with self.e:
            self._dynctx_draw_scene((player_x, player_y))

    def _dynctx_draw_scene(self, player_pos: tuple[int, int]) -> None:
        """Draws a scene in any context."""
        xv_min = player_pos[0] - (c.SCENE_WIDTH / c.TILE_SIZE_ML) / 2
        xv_max = player_pos[0] + (c.SCENE_WIDTH / c.TILE_SIZE_ML) / 2
        yv_min = player_pos[1] - self.player_center_y_offset / c.TILE_SIZE_ML
        yv_max = player_pos[1] + 2

        for ypos, row in enumerate(self.world):
            if not (yv_min <= ypos < yv_max):
                continue
            for xpos, cell in enumerate(row):
                if not (xv_min < xpos < xv_max):
                    continue
                if cell == " ":
                    continue

                color = "black" if cell == "#" else "red"
                tile_x = (xpos - player_pos[0]) * c.TILE_SIZE_ML + self.player_center_x_offset
                tile_y = (ypos - player_pos[1]) * c.TILE_SIZE_ML + self.player_center_y_offset
                self._sc_create_sq_tile(tile_x, tile_y, color)
        self._sc_draw_player()

    def _sc_draw_player(self) -> None:
        """Draws the player."""
        player_x = self.player_center_x_offset
        player_y = self.player_center_y_offset

        self._sc_create_sq_tile(player_x, player_y, c.COLOR_PLAYER)

    def _sc_create_sq_tile(self, x: int, y: int, col: str) -> None:
        """Draw a full-color tile onto the scene."""
        for offset_x in range(c.TILE_SIZE_ML):
            for offset_y in range(c.TILE_SIZE_ML):
                nx = x + offset_x
                ny = y + offset_y
                ui.element("div").style(
                    f"""background-color: {col}; width: {c.TILE_SIZE}px; height: {c.TILE_SIZE}px;
        position: absolute; left: {nx * c.TILE_SIZE}px; top: {ny * c.TILE_SIZE}px;"""
                )
