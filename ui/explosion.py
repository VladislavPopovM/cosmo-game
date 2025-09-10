import curses
from .curses_tools import draw_frame, get_frame_size, sleep
from core import config
import curses

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


async def explode(game, canvas, center_row, center_column):
    """Scene-based explosion animation: update scene only, renderer draws it."""
    curses.beep()
    # Add explosion to scene
    from core.scene import Explosion as ExplosionState
    ex = ExplosionState(center_row=center_row, center_col=center_column, frame_index=0, ticks=0)
    game.scene.explosions.append(ex)

    # Advance frames with delay
    for i in range(len(EXPLOSION_FRAMES)):
        ex.frame_index = i
        # Hold each frame
        await sleep(EXPLOSION_DELAY)
        if game.ended:
            break

    # Remove explosion from scene
    game.scene.explosions = [e for e in game.scene.explosions if e is not ex]
