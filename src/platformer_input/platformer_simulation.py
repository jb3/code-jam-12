import platformer_input.platformer_constants as constants


class PlatformerPhysicsSimulation:
    """The physics simulation."""

    player_x: int
    player_y: int
    _keys: set[str]
    _world: list[list[str]]

    def __init__(self, initial: tuple[int, int]) -> None:
        self.player_x, self.player_y = initial
        self._keys = set()
        self._world = constants.world_grid()
        self._world.reverse()

    def set_held_keys(self, keys: set[str]) -> None:
        """Set the current player-held keys."""
        self._keys = keys

    def tick(self) -> None:
        """Run a tick of the simulation."""
        print(self.player_x, self.player_y)
        if "ArrowRight" in self._keys:
            self.player_x += 1
        if "ArrowLeft" in self._keys:
            self.player_x -= 1
        if "ArrowUp" in self._keys:
            self.player_y -= 1
        if "ArrowDown" in self._keys:
            self.player_y += 1

        print(self.player_x, self.player_y)

    def _collide(self, world: tuple[int, int]) -> bool:
        """Check if a target cell contains a wall."""
        return self._world[world[1]][world[0]] == "#"
