from nicegui import ui

import platformer_input.platformer_constants as c

EMOJIS = {"sky": "\U0001f600", "ground": "\U0001f61e", "letter": "\U0001f636"}


class PlatformerRendererComponent(ui.element):
    """Displays the characters and scene within the game."""

    mask_element: ui.element
    world: list[list[str]]
    letter_el_map: dict[str, ui.label]

    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__("div")
        ui.add_css(""".platformer-input-method-element .tile {
    font-size: 30px;
    margin-top: -7px;
    margin-left: -7px;
    border-radius: 5px;
}
.platformer-input-method-element .tile div {
    transform: translateY(-42px);
    text-align: center;
    color: white;
    font-weight: bold;
    font-size: 1.5rem;
    background-color: #0008;
    border-radius: 100%;
}
.platformer-input-method-element .tile-bounce {
    animation: bounce 200ms ease;
}
@keyframes bounce {
    0% { margin-top: 0; margin-bottom: 0; }
    50% { margin-top: -5px; margin-bottom: 5px; color: cyan; scale: 1.05 }
    100% { margin-top: 0; margin-bottom: 0; }
}
""")
        self.classes("platformer-input-method-element")
        with self:
            self.mask_element = ui.element("div")
        self.mask_element.style(
            f"width: {c.TILE_SIZE * c.SCENE_WIDTH}px; height: {c.TILE_SIZE * c.SCENE_HEIGHT}px;"
            f"background-color: black; position: relative; overflow: hidden"
        )

        self.world = c.world_grid()
        self.world_height = len(self.world)
        self.initial_draw()
        self.move_player(*position)

    def initial_draw(self) -> None:
        """Draw the map for the first time."""
        with self.mask_element:
            self.map_container = ui.element("div")
        self.map_container.style(
            f"position:absolute;width:{len(self.world[0]) * c.TILE_SIZE}px;"
            f"height:{len(self.world) * c.TILE_SIZE}px;"
            f"display:grid;grid-template-columns:repeat({len(self.world[0])}, {c.TILE_SIZE}px);"
            f"grid-template-rows:repeat({len(self.world)}, {c.TILE_SIZE}px);"
            "left: 0; top: 0;"
        )

        self.px_player_offset_lx = ((c.SCENE_WIDTH - 1) * c.TILE_SIZE) / 2
        self.px_player_offset_ty = (c.SCENE_HEIGHT * c.TILE_SIZE) - 2 * c.TILE_SIZE
        with self.mask_element:
            ui.element("div").style(
                f"position:absolute;top:{self.px_player_offset_ty}px;left:{self.px_player_offset_lx}px;"
                f"background-color:{c.COLOR_PLAYER};width:{c.TILE_SIZE}px;height:{c.TILE_SIZE}px"
            )

        self.letter_el_map = {}

        with self.map_container:
            for row in self.world:
                for cell in row:
                    if cell in "# ":
                        emoji = EMOJIS["ground"] if cell == "#" else EMOJIS["sky"]
                        ui.label(emoji).classes("tile")
                    else:
                        with ui.label(EMOJIS["letter"]).classes("tile"):
                            lb = ui.label(cell.replace("<", "\u232b"))
                            self.letter_el_map[cell] = lb

    def move_player(self, player_x: float, player_y: float) -> None:
        """Move the player in the renderer."""
        px_left = self.px_player_offset_lx - player_x * c.TILE_SIZE
        px_top = self.px_player_offset_ty - player_y * c.TILE_SIZE

        self.map_container.style(f"transform: translate({px_left}px, {px_top}px)")

    def play_bounce_effect(self, letter: str) -> None:
        """Play a short bounce effect on a letter tile."""
        tile = self.letter_el_map.get(letter)
        if tile is None:
            return
        tile.classes("tile-bounce")
        ui.timer(0.2, lambda: tile.classes(remove="tile-bounce"), once=True)
