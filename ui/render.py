import curses
from core import config
from ui.curses_tools import draw_frame, get_frame_size
from ui.explosion import EXPLOSION_FRAMES


def render_scene(canvas, scene):
    rows, cols = canvas.getmaxyx()

    # End screen overrides everything
    if scene.end_text:
        text_attr = curses.color_pair(config.COLOR_PAIR_TEXT) | curses.A_BOLD
        txt = scene.end_text
        row = rows // 2
        col = cols // 2 - len(txt) // 2
        canvas.addstr(row, col, txt, text_attr)
        return

    # Stars (phases control brightness)
    star_color = curses.color_pair(config.COLOR_PAIR_STARS)
    for s in scene.stars:
        if s.phase == 0:
            attr = star_color | curses.A_DIM
        elif s.phase == 1:
            attr = star_color
        elif s.phase == 2:
            attr = star_color | curses.A_BOLD
        else:
            attr = star_color
        canvas.addstr(s.row, s.col, s.symbol, attr)

    # Garbage under bullets/spaceship
    garbage_attr = curses.color_pair(config.COLOR_PAIR_GARBAGE)
    for g in scene.garbages:
        draw_frame(canvas, g.row, g.col, g.frame, attr=garbage_attr)

    # Bullets
    bullet_attr = curses.color_pair(config.COLOR_PAIR_TEXT) | curses.A_BOLD
    for b in scene.bullets:
        canvas.addstr(round(b.row), round(b.col), '|', bullet_attr)

    # Spaceship
    if scene.spaceship:
        ship_attr = curses.color_pair(config.COLOR_PAIR_SPACESHIP) | curses.A_BOLD
        draw_frame(canvas, scene.spaceship.row, scene.spaceship.col, scene.spaceship.frame, attr=ship_attr)

    # Explosions on top
    boom_attr = curses.color_pair(config.COLOR_PAIR_EXPLOSION) | curses.A_BOLD
    for ex in scene.explosions:
        frame = EXPLOSION_FRAMES[ex.frame_index % len(EXPLOSION_FRAMES)]
        fr, fc = get_frame_size(frame)
        corner_row = int(ex.center_row - fr / 2)
        corner_col = int(ex.center_col - fc / 2)
        draw_frame(canvas, corner_row, corner_col, frame, attr=boom_attr)

    # Year and phrase
    text_attr = curses.color_pair(config.COLOR_PAIR_TEXT) | curses.A_BOLD
    year_str = str(scene.year)
    year_row = rows - config.BORDER_THICKNESS
    year_col = cols // 2 - len(year_str) // 2
    canvas.addstr(year_row, year_col, year_str, text_attr)
    if scene.phrase:
        phrase_row = year_row - 1
        phrase_col = cols // 2 - len(scene.phrase) // 2
        canvas.addstr(phrase_row, phrase_col, scene.phrase, text_attr)

