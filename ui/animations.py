import curses
from core.scene import Bullet, Garbage, Explosion

from .curses_tools import (
    draw_frame,
    read_controls,
    is_frame_go_out_of_bounds,
    sleep,
    read_file,
    get_frame_size,
    has_collision,
    get_frame_center_coordinate,
)
from core.physics import update_speed
from entities.obstacles import Obstacle
from .explosion import explode
from core import config


BLINK_STAR_DELAY = {
    'A_DIM': 80,   # ~0.96s at TIC_TIMEOUT=0.012
    'A_BOLD': 10,  # ~0.12s
    'STANDARD': 15 # ~0.18s
}

GAMEOVER_FRAME = read_file('frames/gameover.txt')
SPACESHIP_START_FRAME = read_file('frames/rocket_frame_1.txt')
SPACESHIP_END_FRAME = read_file('frames/rocket_frame_2.txt')
SPACESHIP_FRAME = SPACESHIP_START_FRAME


async def blink(canvas, game, star, delay_before_start):
    """Scene-based star blink: update phase, renderer draws it."""
    await sleep(delay_before_start)
    while True:
        if game.ended:
            return
        star.phase = 0
        await sleep(BLINK_STAR_DELAY['A_DIM'])
        star.phase = 1
        await sleep(BLINK_STAR_DELAY['STANDARD'])
        star.phase = 2
        await sleep(BLINK_STAR_DELAY['A_BOLD'])
        star.phase = 1
        await sleep(BLINK_STAR_DELAY['STANDARD'])


async def fire(canvas, game, start_row, start_column, rows_speed=config.BULLET_ROW_SPEED, columns_speed=0):
    """Scene-based bullet movement; renderer draws '|' each tick."""
    row, column = start_row, start_column
    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1
    curses.beep()
    bullet = Bullet(row=row, col=column)
    game.scene.bullets.append(bullet)
    while 0 < bullet.row < max_row and 0 < bullet.col < max_column:
        if game.ended:
            break
        await sleep(1)
        bullet.row += rows_speed
        bullet.col += columns_speed
        obstacle = has_collision(game.obstacles, obj_corner_row=bullet.row, obj_corner_column=bullet.col)
        if obstacle:
            game.obstacles_in_last_collisions.append(obstacle)
            break
    # Remove bullet
    game.scene.bullets = [b for b in game.scene.bullets if b is not bullet]


async def run_spaceship(game, canvas, start_row, start_column):
    """Smooth per-tick movement; animate frame at a slower cadence."""
    frame_rows, frame_cols = get_frame_size(SPACESHIP_FRAME)
    is_inside_canvas = is_frame_go_out_of_bounds(canvas, SPACESHIP_FRAME)
    row_speed = column_speed = 0
    anim_counter = 0
    while True:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)

        if space_pressed:
            game.create_task(fire(canvas, game, start_row, start_column))

        row_speed, column_speed = update_speed(
            row_speed,
            column_speed,
            rows_direction,
            columns_direction,
            row_speed_limit=config.SPACESHIP_ROW_SPEED_LIMIT,
            column_speed_limit=config.SPACESHIP_COL_SPEED_LIMIT,
            fading=config.SPACESHIP_FADING,
        )

        if is_inside_canvas(start_row, start_column, row_speed, column_speed):
            start_row += row_speed
            start_column += column_speed

        # Update scene spaceship position
        if game.scene.spaceship:
            game.scene.spaceship.row = start_row
            game.scene.spaceship.col = start_column

        # Animate frame less frequently for stability
        anim_counter += 1
        if anim_counter >= max(1, int(config.SPACESHIP_DRAW_DELAY)):
            await animate_spaceship()
            if game.scene.spaceship:
                game.scene.spaceship.frame = SPACESHIP_FRAME
            anim_counter = 0

        # Collision check each tick
        obstacle = has_collision(
            game.obstacles,
            obj_corner_row=start_row,
            obj_corner_column=start_column,
            obj_size_rows=frame_rows,
            obj_size_columns=frame_cols)
        if obstacle:
            await game.end_game()
            return

        # Per-tick pacing (keeps movement smooth)
        await sleep(1)


async def animate_spaceship():
    global SPACESHIP_FRAME
    if SPACESHIP_FRAME == SPACESHIP_START_FRAME:
        SPACESHIP_FRAME = SPACESHIP_END_FRAME
    else:
        SPACESHIP_FRAME = SPACESHIP_START_FRAME


async def fly_garbage(canvas, game, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    rows_size, columns_size = get_frame_size(garbage_frame)
    obstacle = Obstacle(row, column, rows_size, columns_size)
    game.obstacles.append(obstacle)

    gobj = Garbage(row=row, col=column, frame=garbage_frame, uid=id(obstacle))
    game.scene.garbages.append(gobj)
    while row < rows_number:
        if game.ended:
            break
        await sleep(1)
        row += speed
        obstacle.row = row
        gobj.row = row
        if obstacle in game.obstacles_in_last_collisions:
            game.obstacles_in_last_collisions.remove(obstacle)
            # Add explosion state; renderer will draw frames
            game.scene.explosions.append(Explosion(center_row=int(row + rows_size // 2), center_col=int(column + columns_size // 2), frame_index=0))
            # Advance explosion frames asynchronously
            game.create_task(_run_explosion(game))
            break
    game.obstacles.remove(obstacle)
    # Remove garbage from scene
    game.scene.garbages = [gg for gg in game.scene.garbages if gg is not gobj]
    return


async def _run_explosion(game):
    from ui.explosion import EXPLOSION_FRAMES
    # Advance all active explosions' frames synchronously each tick
    for i in range(len(EXPLOSION_FRAMES)):
        if game.ended:
            return
        for ex in list(game.scene.explosions):
            ex.frame_index = i
        await sleep(config.EXPLOSION_DELAY_TICS)
    game.scene.explosions.clear()


async def show_gameover(canvas):
    # After end_game, we render just once (The END is handled by Game)
    await sleep(1)
