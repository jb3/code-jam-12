import math
import time

import platformer_input.platformer_constants as constants

EPSILON = 1e-6


class PlatformerPhysicsSimulation:
    """The physics simulation."""

    player_x: float
    player_y: float

    _xvel: float
    _yvel: float

    _deltatime: float
    _last_tick_at: float

    _keys: set[str]
    _world: list[list[bool]]

    def __init__(self, initial: tuple[int, int]) -> None:
        self.player_x, self.player_y = initial
        self._xvel = 0
        self._yvel = 0

        self._deltatime = 0
        self._last_tick_at = 0

        self._keys = set()
        # turn into mask for efficient access
        self._world = []
        world = constants.world_grid()
        self._world = [[cell == "#" for cell in row] for row in world]

    def set_held_keys(self, keys: set[str]) -> None:
        """Set the current player-held keys."""
        self._keys = keys

    def tick(self) -> None:
        """Run a tick of the simulation."""
        current_time = time.perf_counter()
        if self._last_tick_at == 0:
            self._last_tick_at = current_time
        self._deltatime = current_time - self._last_tick_at
        self._last_tick_at = current_time

        delta_accel = self._deltatime * constants.ACCEL_SPEED

        if "ArrowRight" in self._keys:
            self._xvel = min(constants.MOV_SPEED, self._xvel + delta_accel)
        if "ArrowLeft" in self._keys:
            self._xvel = max(-constants.MOV_SPEED, self._xvel - delta_accel)
        if "ArrowUp" in self._keys and self._collide((self.player_x, self.player_y + 2 * EPSILON)):
            self._yvel = -constants.JUMP_FORCE

        self._apply_x_velocity()
        self._apply_y_velocity()

    def _apply_x_velocity(self) -> None:
        """Apply horizontal velocity and decay."""
        decay_factor = 1 - constants.VELOCITY_DECAY_RATE * self._deltatime
        decay_factor = max(decay_factor, 0)
        self._xvel *= decay_factor
        dx = self._xvel * self._deltatime
        if dx != 0:
            new_x = self.player_x + dx
            if self._collide((new_x, self.player_y)):
                self._xvel = 0
                if dx > 0:
                    player_edge_r = self.player_x + 1
                    tile_edge = int(player_edge_r)
                    new_x = tile_edge - EPSILON
                else:
                    tile_edge = int(self.player_x)
                    new_x = tile_edge + EPSILON
            self.player_x = new_x

    def _apply_y_velocity(self) -> None:
        """Apply gravity and vertical player clamping."""
        self._yvel += constants.GRAVITY_FORCE * self._deltatime
        dy = self._yvel * self._deltatime
        if dy != 0:
            new_y = self.player_y + dy
            if self._collide((self.player_x, new_y)):
                self._yvel = 0
                if dy > 0:
                    player_edge_b = self.player_y + 1
                    tile_edge = int(player_edge_b)
                    new_y = tile_edge - EPSILON
                else:
                    tile_edge = int(self.player_y)
                    new_y = tile_edge + EPSILON
            self.player_y = new_y

    def _collide(self, player: tuple[float, float]) -> bool:
        """Check if a target cell contains a wall."""
        player_left = player[0]
        player_right = player[0] + 1
        player_top = player[1]
        player_bottom = player[1] + 1

        left_tile = math.floor(player_left)
        right_tile = math.floor(player_right - EPSILON)
        top_tile = math.floor(player_top)
        bottom_tile = math.floor(player_bottom - EPSILON)

        for tile_y in range(top_tile, bottom_tile + 1):
            for tile_x in range(left_tile, right_tile + 1):
                in_map = 0 <= tile_y < len(self._world) and 0 <= tile_x < len(self._world[0])
                if not in_map:
                    continue
                if self._world[tile_y][tile_x]:
                    return True
        return False
