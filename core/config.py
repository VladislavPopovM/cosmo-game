TIC_TIMEOUT = 0.04
STARS_COUNT = 300
SYMBOLS_FOR_STARS = '*'
DELAY_BEFORE_START_BLINK_STAR = (15, 800)
BORDER_THICKNESS = 2
GARBAGES_PATH = 'frames/garbage'
# Slower garbage speed for smoother motion
# Even slower garbage speed for smoother motion
GARBAGE_RANGE_SPEED = (0.0005, 0.002)
DELAY_BETWEEN_YEAR = 1500
START_YEAR = 1957
SPACESHIP_DRAW_DELAY = 35

# Color pair ids (initialized at runtime)
COLOR_PAIR_STARS = 1
COLOR_PAIR_SPACESHIP = 2
COLOR_PAIR_GARBAGE = 3
COLOR_PAIR_TEXT = 4
COLOR_PAIR_EXPLOSION = 5

# Limit concurrent garbage pieces on screen
MAX_GARBAGE = 6

# Explosion pacing (in tics)
EXPLOSION_DELAY_TICS = 60

# Bullet speed (negative moves up). Closer to 0 -> slower.
BULLET_ROW_SPEED = -0.02

# Render layers (higher draws above lower)
LAYER_STARS = 10
LAYER_GARBAGE = 30
LAYER_BULLET = 40
LAYER_SPACESHIP = 50
LAYER_EXPLOSION = 60
LAYER_TEXT = 70

# Spaceship control tuning
SPACESHIP_ROW_SPEED_LIMIT = 1.0
SPACESHIP_COL_SPEED_LIMIT = 1.0
SPACESHIP_FADING = 0.7
