# 
#  config.py    All tunable game constants
# 

# Window
WINDOW_WIDTH  = 480
WINDOW_HEIGHT = 700
FPS           = 60
TITLE         = "Flappy Elon"

# Physics
GRAVITY        = 0.5    # pixels added to fall speed each frame
JUMP_STRENGTH  = -9     # upward velocity on flap (negative = up)
MAX_FALL_SPEED = 10     # terminal velocity

# Bird
BIRD_WIDTH  = 55
BIRD_HEIGHT = 55
BIRD_START_X = 100
BIRD_START_Y = 300

# Pipes
PIPE_WIDTH       = 80          # rendered width
PIPE_GAP         = 160         # vertical gap between top & bottom pipe
PIPE_SPEED       = 3           # pixels per frame (base speed)
PIPE_SPAWN_MS    = 1500        # milliseconds between spawns
PIPE_MIN_HEIGHT  = 60          # minimum top-pipe height
PIPE_MAX_HEIGHT  = 350         # maximum top-pipe height

# Ground
GROUND_HEIGHT  = 100           # how many px from bottom the ground occupies
GROUND_SPEED   = 3             # must match PIPE_SPEED

# Scoring & difficulty
POINTS_PER_PIPE         = 1
SPEED_INCREMENT         = 0.3  # added to speed every 10 points
SPEED_INCREMENT_EVERY   = 10   # score interval for difficulty bump
MAX_SPEED               = 7    # hard cap

# Colours (fallback / UI)
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
YELLOW = (255, 220, 50)
RED    = (220, 50,  50)
SKY    = (112, 197, 255)       # procedural background colour

# Asset paths
import os
BASE_DIR    = os.path.dirname(__file__)
ASSETS      = os.path.join(BASE_DIR, "assets")
IMG_DIR     = os.path.join(ASSETS, "images")
AUDIO_DIR   = os.path.join(ASSETS, "audio")
FONT_DIR    = os.path.join(ASSETS, "fonts")

IMG_BIRD    = os.path.join(IMG_DIR,   "elon_bird.png")
IMG_PIPE    = os.path.join(IMG_DIR,   "pipe.png")
IMG_GROUND  = os.path.join(IMG_DIR,   "ground.png")
IMG_BG      = os.path.join(IMG_DIR,   "background.png")   # optional  drop in if you have one

SFX_FLAP    = os.path.join(AUDIO_DIR, "flap.ogg")
SFX_SCORE   = os.path.join(AUDIO_DIR, "score.ogg")
SFX_HIT     = os.path.join(AUDIO_DIR, "hit.ogg")
BGM_TRACK   = os.path.join(AUDIO_DIR, "bgm.ogg")