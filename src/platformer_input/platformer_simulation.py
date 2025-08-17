import time

import platformer_input.platformer_constants as constants


class PlatformerPhysicsSimulation:
    """The physics simulation."""

    player_x: float
    player_y: float

    _xvel: float
    _yvel: float

    _deltatime: float
    _last_tick_at: float

    _keys: set[str]
    _world: list[list[str]]

    def __init__(self, initial: tuple[int, int]) -> None:
        self.player_x, self.player_y = initial
        self._xvel = 0
        self._yvel = 0

        self._deltatime = 0
        self._last_tick_at = time.perf_counter()

        self._keys = set()
        self._world = constants.world_grid()
        self._world.reverse()

    def set_held_keys(self, keys: set[str]) -> None:
        """Set the current player-held keys."""
        self._keys = keys

    def tick(self) -> None:
        """Run a tick of the simulation."""
        current_time = time.perf_counter()
        self._deltatime = current_time - self._last_tick_at
        self._last_tick_at = current_time

        delta_accel = self._deltatime * constants.ACCEL_SPEED

        if "ArrowRight" in self._keys:
            self._xvel = min(constants.MOV_SPEED, self._xvel + delta_accel)
        if "ArrowLeft" in self._keys:
            self._xvel = max(-constants.MOV_SPEED, self._xvel - delta_accel)
        if "ArrowUp" in self._keys:
            self._yvel = max(-constants.MOV_SPEED, self._yvel - delta_accel)
        if "ArrowDown" in self._keys:
            self._yvel = min(constants.MOV_SPEED, self._yvel + delta_accel)

        self.player_x += self._xvel
        self.player_y += self._yvel

        decay_factor = 1 - constants.VELOCITY_DECAY_RATE * self._deltatime
        decay_factor = max(decay_factor, 0)
        self._xvel *= decay_factor
        self._yvel *= decay_factor

    def _collide(self, world: tuple[int, int]) -> bool:
        """Check if a target cell contains a wall."""
        return self._world[world[1]][world[0]] == "#"
