import math

RES = WIDTH, HEIGHT = 1300, 800
HWIDTH = WIDTH // 2
HHEIGHT = HEIGHT // 2
FPS = 100  # 30  # ok please fix it so everything isn't flash lightning in my face when not potato mode

PLYR_POS = 1.5, 3.5  # 28, 3.5
PLYR_ANGLE = 0
PLYR_SPD = 0.004
PLYR_RSPD = 0.002
PLYR_SCALE = 60

FOV = math.pi / 3
HFOV = FOV / 2
NUM_RAYS = WIDTH // 2  # 750
HNUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20
SCREEN_DIST = HWIDTH / math.tan(HFOV)
SCALE = WIDTH // NUM_RAYS

MAX_TEX = 2048
HMAX_TEX = MAX_TEX // 2

MOUSE_SENS = 0.0003
MOUSE_MAXREL = 40
MOUSE_LBORD = 500
MOUSE_RBORD = WIDTH - MOUSE_LBORD
