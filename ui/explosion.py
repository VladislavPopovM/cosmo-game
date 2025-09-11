import curses
from .curses_tools import draw_frame, get_frame_size, sleep
from core import config

EXPLOSION_FRAMES = [
    """\
           (_) 
       (  (   (  (
      () (  (  )
        ( )  ()
    """,
    """\
           (_) 
       (  (   (   
         (  (  )
          )  (
    """,
    """\
            (  
          (   (   
         (     (
          )  (
    """,
    """\
            ( 
              (
            (  
    """,
]

EXPLOSION_DELAY = config.EXPLOSION_DELAY_TICS


async def explode(canvas, center_row, center_column):
    rows, columns = get_frame_size(EXPLOSION_FRAMES[0])
    corner_row = center_row - rows / 2
    corner_column = center_column - columns / 2

    curses.beep()
    boom_attr = curses.color_pair(config.COLOR_PAIR_EXPLOSION) | curses.A_BOLD
    for frame in EXPLOSION_FRAMES:
        draw_frame(canvas, corner_row, corner_column, frame, attr=boom_attr)
        await sleep(EXPLOSION_DELAY)
        draw_frame(canvas, corner_row, corner_column, frame, negative=True)
        await sleep(EXPLOSION_DELAY)
