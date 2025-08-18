"""Constants for the platformer input method rendering & simulator."""

"""Size in pixels of each "tile"."""
TILE_SIZE = 30
"""Width in tiles of the whole scene."""
SCENE_WIDTH = 16
"""Height in tiles of the whole scene."""
SCENE_HEIGHT = 9

JUMP_FORCE = 14
"""Max player speed."""
MOV_SPEED = 200
"""How fast the player accelerates."""
ACCEL_SPEED = 150
"""Essentially friction simulation"""
VELOCITY_DECAY_RATE = 10
"""Gravity force"""
GRAVITY_FORCE = 17

COLOR_PLAYER = "purple"


SCENE = """#############################################
#                                           #
#                                           #
#  u  v  w  x  y             z  .  !  _  <  #
#                                           #
#                                           #
#                         ###################
##################                          #
#   k  l  m  n  o          p  q  r  s  t    #
#                                           #
#                                           #
#  ################      ###############    #
#                                           #
#   a  b  c  d  e         f  g  h  i  j     #
#                                           #
#                                           #
#############################################
"""


def world_grid() -> list[list[str]]:
    """Get a grid of one-character `str`s representing the scene as a grid."""
    lines = SCENE.splitlines()
    max_length = max(len(ln) for ln in lines)

    grid = []
    for line in lines:
        lst = list(line)
        if len(line) < max_length:
            lst.extend(" " for _ in range(max_length - len(line)))
        grid.append(lst)

    return grid
