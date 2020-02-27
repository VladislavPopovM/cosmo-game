import time
import random
import curses

from curses_tools import get_garbages_frames, get_frame_size, sleep, get_frame_center_coordinate
from animations import blink, fly_garbage, run_spaceship, coroutines, SPACESHIP_FRAME
from game_scenario import get_garbage_delay_tics

TIC_TIMEOUT = 0.00001
STARS_COUNT = 500
SYMBOLS_FOR_STARS = '+*.:'
DELAY_BEFORE_START_BLINK_STAR = (15, 800)
BORDER_THICKNESS = 2
GARBAGES_FRAMES = get_garbages_frames('frames/garbage')
garbage_count = 25
GARBAGE_RANGE_SPEED = (0.005, 0.02)
DELAY_BETWEEN_YEAR = 1500
year = 1957


async def show_year(canvas):
    height_canvas, width_canvas = canvas.getmaxyx()
    center_canvas = (height_canvas - BORDER_THICKNESS, width_canvas // 2)
    canvas.derwin(*center_canvas)
    while True:
        canvas.addstr(*center_canvas, str(year))
        await sleep()


async def increase_year_after_delay():
    global year
    while True:
        await sleep(DELAY_BETWEEN_YEAR)
        year += 1


async def fill_orbit_with_garbage(canvas):
    height_canvas, width_canvas = canvas.getmaxyx()
    while True:
        garbage_frame = random.choice(GARBAGES_FRAMES)
        cols_garbage_frame, _ = get_frame_size(garbage_frame)
        column = random.randint(BORDER_THICKNESS, width_canvas - cols_garbage_frame * 3)
        speed = random.uniform(*GARBAGE_RANGE_SPEED)
        await fly_garbage(canvas, column=column, garbage_frame=garbage_frame, speed=speed)
        await sleep()


def generate_stars(canvas, star_count=STARS_COUNT, kinds_stars=SYMBOLS_FOR_STARS):
    height_canvas, width_canvas = canvas.getmaxyx()
    return [blink(canvas,
                  row=random.randint(BORDER_THICKNESS, height_canvas - BORDER_THICKNESS),
                  column=random.randint(BORDER_THICKNESS, width_canvas - BORDER_THICKNESS),
                  delay_before_start=random.randint(*DELAY_BEFORE_START_BLINK_STAR),
                  symbol=random.choice(kinds_stars))
            for _ in range(star_count)]


async def generate_garbage(canvas):
    while True:
        delay_tics = get_garbage_delay_tics(year)
        if delay_tics:
            coroutines.append(fill_orbit_with_garbage(canvas))
        await sleep(delay_tics or 1)


def generate_spaceship(canvas):
    center_height, center_width = get_frame_center_coordinate(canvas, SPACESHIP_FRAME)
    return run_spaceship(
        canvas,
        start_row=center_height,
        start_column=center_width,
    )


def draw(canvas):
    canvas.border()
    canvas.refresh()
    canvas.nodelay(True)

    coroutines.extend(generate_stars(canvas))
    coroutines.append(generate_spaceship(canvas))
    coroutines.append(generate_garbage(canvas))
    coroutines.append(show_year(canvas))
    coroutines.append(increase_year_after_delay())

    while True:
        for coroutine in coroutines[:]:
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
    curses.curs_set(False)
