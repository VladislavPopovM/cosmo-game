import asyncio
import curses

from curses_tools import draw_frame, read_controls, is_frame_go_out_of_bounds


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

    for i in range(delay_before_start):
        await asyncio.sleep(0)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for i in range(BLINK_STAR_DELAY['A_DIM']):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(BLINK_STAR_DELAY['STANDARD']):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for i in range(BLINK_STAR_DELAY['A_BOLD']):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(BLINK_STAR_DELAY['STANDARD']):
            await asyncio.sleep(0)


async def fire(canvas, start_row, start_column, rows_speed=-0.03, columns_speed=0):
    """Display animation of gun shot. Direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
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
        for i in range(SPACESHIP_DRAW_DELAY['START_FRAME']):
            await asyncio.sleep(0)

        draw_frame(canvas, start_row, start_column, start_frame, negative=True)
        await asyncio.sleep(0)

        draw_frame(canvas, start_row, start_column, end_frame)
        for i in range(SPACESHIP_DRAW_DELAY['END_FRAME']):
            await asyncio.sleep(0)

        draw_frame(canvas, start_row, start_column, end_frame, negative=True)
        await asyncio.sleep(0)
