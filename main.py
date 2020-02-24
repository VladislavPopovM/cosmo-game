import time
import random
import curses

from curses_tools import get_garbages_frames, get_frame_size, sleep
from animations import blink, fly_garbage, run_spaceship

TIC_TIMEOUT = 0.00001
STAR_COUNT = 500
SYMBOLS_FOR_STARS = '+*.:'
DELAY_BEFORE_START_BLINK_STAR = (15, 800)
BORDER_THICKNESS = 2
GARBAGES_FRAMES = get_garbages_frames('frames/garbage')
GARAGE_COUNT = 30
GARBAGE_RANGE_SPEED = (0.005, 0.02)
DELAY_BEFORE_CREATE_GARBAGE = (300, 500)
COROUTINES = []


async def fill_orbit_with_garbage(canvas):
    height_canvas, width_canvas = canvas.getmaxyx()
    while True:
        garbage_frame = random.choice(GARBAGES_FRAMES)
        cols_garbage_frame, _ = get_frame_size(garbage_frame)
        column = random.randint(BORDER_THICKNESS, width_canvas - cols_garbage_frame * 3)
        speed = random.uniform(*GARBAGE_RANGE_SPEED)
        await sleep(random.randint(*DELAY_BEFORE_CREATE_GARBAGE))
        await fly_garbage(canvas, column, garbage_frame, speed)


def generate_stars(canvas, star_count=STAR_COUNT, kinds_stars=SYMBOLS_FOR_STARS):
    height_canvas, width_canvas = canvas.getmaxyx()
    stars = []
    for _ in range(star_count):
        row = random.randint(BORDER_THICKNESS, height_canvas - BORDER_THICKNESS)
        col = random.randint(BORDER_THICKNESS, width_canvas - BORDER_THICKNESS)
        star = blink(
            canvas, row, col,
            delay_before_start=random.randint(*DELAY_BEFORE_START_BLINK_STAR),
            symbol=random.choice(kinds_stars)
        )
        stars.append(star)
    return stars


def generate_garbages(canvas, garbage_count=GARAGE_COUNT):
    garbages = []
    for _ in range(garbage_count):
        garbages.append(fill_orbit_with_garbage(canvas))
    return garbages


def generate_spaceship(canvas):
    height_canvas, width_canvas = canvas.getmaxyx()
    center_height = height_canvas // 2
    width_height = width_canvas // 2
    return run_spaceship(
        canvas,
        start_row=center_height,
        start_column=width_height,
        coroutines=COROUTINES,
    )


def draw(canvas):
    canvas.border()
    canvas.refresh()
    canvas.nodelay(True)

    COROUTINES.extend(generate_stars(canvas))
    COROUTINES.append(generate_spaceship(canvas))
    COROUTINES.extend(generate_garbages(canvas))

    while True:
        for coroutine in COROUTINES[:]:
            try:
                coroutine.send(None)
            except StopIteration:
                COROUTINES.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
    curses.curs_set(False)
