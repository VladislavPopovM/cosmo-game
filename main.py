import asyncio
import curses

from core.game import Game


def main(canvas):
    curses.curs_set(False)
    game = Game(canvas)
    asyncio.run(game.run())


if __name__ == "__main__":
    curses.wrapper(main)
