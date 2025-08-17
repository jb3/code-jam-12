import typing

import nicegui.events
from nicegui import ui

import input_method_proto
from platformer_input.platformer_scene_cmp import PlatformerSceneComponent
from platformer_input.platformer_simulation import PlatformerPhysicsSimulation

ALLOWED_KEYS = ("ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Shift", " ", "Enter")
INITIAL_POS = (1, 10)
FPS = 144


class PlatformerInputMethod(input_method_proto.IInputMethod):
    """The platformer input method.

    Users will control a 2D platformer player to move around and bump into blocks
    to enter characters.
    """

    callbacks: list[typing.Callable[[str], None]]
    scene: PlatformerSceneComponent
    held_keys: set[str]

    def __init__(self) -> None:
        self.callbacks = []
        self.scene = PlatformerSceneComponent(INITIAL_POS)
        self.physics = PlatformerPhysicsSimulation(INITIAL_POS)
        self.held_keys = set()
        ui.keyboard(lambda e: self.keyboard_handler(e))
        ui.timer(1 / FPS, lambda: self._hinterv())

    def keyboard_handler(self, event: nicegui.events.KeyEventArguments) -> None:
        """Call with the nicegui keyboard callback."""
        evk = str(event.key)
        if event.action.repeat or evk not in ALLOWED_KEYS:
            return

        if event.action.keydown:
            self.held_keys.add(evk)
        elif event.action.keyup and evk in self.held_keys:
            self.held_keys.remove(evk)
        self.physics.set_held_keys(self.held_keys)

    def _hinterv(self) -> None:
        """Run every game tick."""
        self.physics.tick()
        self.scene.move_player(self.physics.player_x, self.physics.player_y)

    def on_text_update(self, callback: typing.Callable[[str], None]) -> None:
        """Call `callback` every time the user input changes."""
        self.callbacks.append(callback)
