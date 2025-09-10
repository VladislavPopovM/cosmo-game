import asyncio
import curses
import locale

from core.game import Game


def main(canvas):
    # Enable locale so Unicode glyphs render correctly (if terminal supports)
    try:
        locale.setlocale(locale.LC_ALL, '')
    except Exception:
        pass
    curses.curs_set(False)
    game = Game(canvas)
    asyncio.run(game.run())


if __name__ == "__main__":
    curses.wrapper(main)
