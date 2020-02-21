import asyncio
import curses

from curses_tools import draw_frame, read_controls, is_frame_go_out_of_bounds, sleep


BLINK_STAR_DELAY = {
    'A_DIM': 700,
    'A_BOLD': 40,
    'STANDARD': 50,
}

SPACESHIP_DRAW_DELAY = {
    'START_FRAME': 20,
    'END_FRAME': 20,
}


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


async def fire(canvas, start_row, start_column, rows_speed=-0.03, columns_speed=0):
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


async def animate_spaceship(canvas, start_row, start_column, start_frame, end_frame):
    is_inside_canvas = is_frame_go_out_of_bounds(canvas, start_frame)

    while True:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)

        if is_inside_canvas(start_row, start_column, rows_direction, columns_direction):
            start_row += rows_direction
            start_column += columns_direction

        draw_frame(canvas, start_row, start_column, start_frame)
        await sleep(SPACESHIP_DRAW_DELAY['START_FRAME'])

        draw_frame(canvas, start_row, start_column, start_frame, negative=True)
        await sleep(1)

        draw_frame(canvas, start_row, start_column, end_frame)
        await sleep(SPACESHIP_DRAW_DELAY['END_FRAME'])

        draw_frame(canvas, start_row, start_column, end_frame, negative=True)
        await sleep(1)


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

