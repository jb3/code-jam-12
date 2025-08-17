TILE_SIZE = 10
SCENE_WIDTH = 45
SCENE_HEIGHT = 30
TILE_SIZE_ML = 3

JUMP_FORCE = 5
MOV_SPEED = 10

COLOR_BG = "skyblue"
COLOR_PLAYER = "purple"
COLOR_GROUND = "#181818"


SCENE = """######################################
     u  v  w  x      y  z  .  !  ,

    ############    ##############

    k  l  m  n  o  p  q  r  s  t

  ##############    ################

      a  b  c  d  e  f  g  h  i  j

######################################
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
