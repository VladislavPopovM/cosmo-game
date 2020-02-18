import time
import random
import curses

from curses_tools import read_file
from animations import blink, animate_spaceship

TIC_TIMEOUT = 0.00001
START_FRAME_SPACESHIP = read_file('frames/rocket_frame_1.txt')
END_FRAME_SPACESHIP = read_file('frames/rocket_frame_2.txt')
STAR_COUNT = 500
SYMBOLS_FOR_STARS = '+*.:'
DELAY_BEFORE_START_BLINK_STAR = (15, 800)


def generate_stars(canvas, count_stars=500, kinds_stars='+*.:'):
    height_canvas, width_canvas = canvas.getmaxyx()
    stars = []
    border_thickness = 2
    for _ in range(count_stars):
        row = random.randint(border_thickness, height_canvas - border_thickness)
        col = random.randint(border_thickness, width_canvas - border_thickness)
        star = blink(
            canvas, row, col,
            delay_before_start=random.randint(*DELAY_BEFORE_START_BLINK_STAR),
            symbol=random.choice(kinds_stars)
        )
        stars.append(star)
    return stars


def draw(canvas):
    canvas.border()
    canvas.refresh()
    canvas.nodelay(True)
    height_canvas, width_canvas = canvas.getmaxyx()
    coroutines = generate_stars(canvas, STAR_COUNT, SYMBOLS_FOR_STARS)
    center_height = height_canvas // 2
    width_height = width_canvas // 2
    spaceship = animate_spaceship(
        canvas,
        start_row=center_height,
        start_column=width_height,
        start_frame=START_FRAME_SPACESHIP,
        end_frame=END_FRAME_SPACESHIP)
    coroutines.append(spaceship)

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
