import time
import random
import curses

from curses_tools import get_garbages_frames, get_frame_size, sleep, get_coordinate_center_frame
from animations import blink, fly_garbage, run_spaceship, COROUTINES, SPACESHIP_FRAME
from game_scenario import get_garbage_delay_tics, PHRASES

TIC_TIMEOUT = 0.00001
STAR_COUNT = 500
SYMBOLS_FOR_STARS = '+*.:'
DELAY_BEFORE_START_BLINK_STAR = (15, 800)
BORDER_THICKNESS = 2
GARBAGES_FRAMES = get_garbages_frames('frames/garbage')
GARBAGE_COUNT = 40
GARBAGE_RANGE_SPEED = (0.005, 0.02)
DELAY_BEFORE_CREATE_GARBAGE = (300, 500)
YEAR = 1957
DELAY_BETWEEN_YEAR = 1500


async def show_year(canvas):
    height_canvas, width_canvas = canvas.getmaxyx()
    center_canvas = (height_canvas - BORDER_THICKNESS, width_canvas // 2)
    canvas.derwin(*center_canvas)
    while True:
        message = '{} {}'.format(YEAR, PHRASES.get(YEAR, ''))
        canvas.addstr(*center_canvas, message)
        await sleep()


async def increase_year_after_delay():
    global YEAR
    global GARBAGE_COUNT
    while True:
        await sleep(DELAY_BETWEEN_YEAR)
        YEAR += 1
        GARBAGE_COUNT += 1


async def fill_orbit_with_garbage(canvas):
    height_canvas, width_canvas = canvas.getmaxyx()
    while True:
        garbage_frame = random.choice(GARBAGES_FRAMES)
        cols_garbage_frame, _ = get_frame_size(garbage_frame)
        column = random.randint(BORDER_THICKNESS, width_canvas - cols_garbage_frame * 3)
        speed = random.uniform(*GARBAGE_RANGE_SPEED)
        delay_tics = get_garbage_delay_tics(YEAR)
        if delay_tics:
            await sleep(delay_tics)
            await fly_garbage(canvas, column=column, garbage_frame=garbage_frame, speed=speed)
        await sleep()


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


def generate_garbages(canvas, garbage_count=GARBAGE_COUNT):
    garbages = []
    for _ in range(garbage_count):
        garbages.append(fill_orbit_with_garbage(canvas))
    return garbages


def generate_spaceship(canvas):
    center_height, center_width = get_coordinate_center_frame(canvas, SPACESHIP_FRAME)
    return run_spaceship(
        canvas,
        start_row=center_height,
        start_column=center_width,
    )


def draw(canvas):
    canvas.border()
    canvas.refresh()
    canvas.nodelay(True)

    COROUTINES.extend(generate_stars(canvas))
    COROUTINES.append(generate_spaceship(canvas))
    COROUTINES.extend(generate_garbages(canvas))
    COROUTINES.append(show_year(canvas))
    COROUTINES.append(increase_year_after_delay())

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
