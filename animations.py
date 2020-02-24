import curses

from curses_tools import draw_frame, read_controls, is_frame_go_out_of_bounds, sleep, read_file
from physics import update_speed


BLINK_STAR_DELAY = {
    'A_DIM': 700,
    'A_BOLD': 40,
    'STANDARD': 50,
}

SPACESHIP_DRAW_DELAY = 20

START_FRAME_SPACESHIP = read_file('frames/rocket_frame_1.txt')
END_FRAME_SPACESHIP = read_file('frames/rocket_frame_2.txt')

SPACESHIP_FRAME = START_FRAME_SPACESHIP


async def blink(canvas, row, column, delay_before_start, symbol='*'):
    """Display star. Symbol and position can be specified."""

    await sleep(delay_before_start)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(BLINK_STAR_DELAY['A_DIM'])

        canvas.addstr(row, column, symbol)
        await sleep(BLINK_STAR_DELAY['STANDARD'])

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(BLINK_STAR_DELAY['A_BOLD'])

        canvas.addstr(row, column, symbol)
        await sleep(BLINK_STAR_DELAY['STANDARD'])


async def fire(canvas, start_row, start_column, rows_speed=-0.1, columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await sleep(1)

    canvas.addstr(round(row), round(column), 'O')
    await sleep(1)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await sleep(1)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def run_spaceship(canvas, start_row, start_column, coroutines):
    is_inside_canvas = is_frame_go_out_of_bounds(canvas, SPACESHIP_FRAME)
    row_speed = column_speed = 0
    while True:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)

        if space_pressed:
            coroutines.append(fire(canvas, start_row, start_column))

        row_speed, column_speed = update_speed(row_speed, column_speed, rows_direction, columns_direction)

        if is_inside_canvas(start_row, start_column, row_speed, column_speed):
            start_row += row_speed
            start_column += column_speed

        draw_frame(canvas, start_row, start_column, SPACESHIP_FRAME)
        await sleep(SPACESHIP_DRAW_DELAY)

        draw_frame(canvas, start_row, start_column, SPACESHIP_FRAME, negative=True)
        await animate_spaceship()


async def animate_spaceship():
    global SPACESHIP_FRAME
    if SPACESHIP_FRAME == START_FRAME_SPACESHIP:
        SPACESHIP_FRAME = END_FRAME_SPACESHIP
    else:
        SPACESHIP_FRAME = START_FRAME_SPACESHIP


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await sleep(1)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed

