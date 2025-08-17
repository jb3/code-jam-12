import platformer_input.platformer_constants as constants


class PlatformerPhysicsSimulation:
    """The physics simulation."""

    player_x: float
    player_y: float
    _xvel: float
    _yvel: float

    _keys: set[str]
    _world: list[list[str]]

    def __init__(self, initial: tuple[int, int]) -> None:
        self.player_x, self.player_y = initial
        self._xvel = 0
        self._yvel = 0

        self._keys = set()
        self._world = constants.world_grid()
        self._world.reverse()

    def set_held_keys(self, keys: set[str]) -> None:
        """Set the current player-held keys."""
        self._keys = keys

    def tick(self) -> None:
        """Run a tick of the simulation."""
        if "ArrowRight" in self._keys:
            self._xvel = min(constants.MOV_SPEED, self._xvel + constants.ACCEL_SPEED)
        if "ArrowLeft" in self._keys:
            self._xvel = max(-constants.MOV_SPEED, self._xvel - constants.ACCEL_SPEED)
        if "ArrowUp" in self._keys:
            self._yvel = max(-constants.MOV_SPEED, self._yvel - constants.ACCEL_SPEED)
        if "ArrowDown" in self._keys:
            self._yvel = min(constants.MOV_SPEED, self._yvel + constants.ACCEL_SPEED)

        self.player_x += self._xvel / 10
        self.player_y += self._yvel / 10

        self._xvel *= constants.VELOCITY_DECAY_RATE
        self._yvel *= constants.VELOCITY_DECAY_RATE

    def _collide(self, world: tuple[int, int]) -> bool:
        """Check if a target cell contains a wall."""
        return self._world[world[1]][world[0]] == "#"
