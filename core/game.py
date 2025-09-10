import asyncio
import random

from core import config
from core.game_scenario import get_garbage_delay_tics, PHRASES
from ui.curses_tools import (
    get_garbages_frames,
    get_frame_size,
    sleep,
    get_frame_center_coordinate,
)
from ui.animations import blink, fly_garbage, run_spaceship, SPACESHIP_FRAME


class Game:
    def __init__(self, canvas):
        self.canvas = canvas
        self.year = config.START_YEAR
        self.obstacles = []
        self.obstacles_in_last_collisions = []
        self.garbage_frames = get_garbages_frames(config.GARBAGES_PATH)
        self.tasks = []

    def create_task(self, coro):
        task = asyncio.create_task(coro)
        self.tasks.append(task)
        return task

    async def show_year(self):
        height_canvas, width_canvas = self.canvas.getmaxyx()
        row_year = height_canvas - config.BORDER_THICKNESS
        last_phrase_length = 0
        while True:
            year_str = str(self.year)
            col_year = width_canvas // 2 - len(year_str) // 2
            self.canvas.addstr(row_year, col_year, year_str)

            phrase = PHRASES.get(self.year)
            phrase_row = row_year - 1
            if phrase:
                col_phrase = width_canvas // 2 - len(phrase) // 2
                self.canvas.addstr(phrase_row, col_phrase, phrase)
                last_phrase_length = len(phrase)
            else:
                if last_phrase_length:
                    self.canvas.addstr(phrase_row, 0, ' ' * last_phrase_length)
                    last_phrase_length = 0

            await sleep()

    async def increase_year_after_delay(self):
        while True:
            await sleep(config.DELAY_BETWEEN_YEAR)
            self.year += 1

    async def fill_orbit_with_garbage(self):
        height_canvas, width_canvas = self.canvas.getmaxyx()
        garbage_frame = random.choice(self.garbage_frames)
        cols_garbage_frame, _ = get_frame_size(garbage_frame)
        column = random.randint(
            config.BORDER_THICKNESS, width_canvas - cols_garbage_frame * 3
        )
        speed = random.uniform(*config.GARBAGE_RANGE_SPEED)
        await fly_garbage(
            self.canvas, self, column=column, garbage_frame=garbage_frame, speed=speed
        )
        await sleep()

    def generate_stars(self):
        height_canvas, width_canvas = self.canvas.getmaxyx()
        return [
            blink(
                self.canvas,
                row=random.randint(
                    config.BORDER_THICKNESS, height_canvas - config.BORDER_THICKNESS
                ),
                column=random.randint(
                    config.BORDER_THICKNESS, width_canvas - config.BORDER_THICKNESS
                ),
                delay_before_start=random.randint(*config.DELAY_BEFORE_START_BLINK_STAR),
                symbol=random.choice(config.SYMBOLS_FOR_STARS),
            )
            for _ in range(config.STARS_COUNT)
        ]

    async def generate_garbage(self):
        while True:
            delay_tics = get_garbage_delay_tics(self.year)
            if delay_tics:
                self.create_task(self.fill_orbit_with_garbage())
            await sleep(delay_tics or 1)

    async def refresh(self):
        while True:
            self.canvas.refresh()
            await asyncio.sleep(config.TIC_TIMEOUT)

    async def run(self):
        self.canvas.border()
        self.canvas.nodelay(True)

        for star in self.generate_stars():
            self.create_task(star)

        center_height, center_width = get_frame_center_coordinate(
            self.canvas, SPACESHIP_FRAME
        )
        self.create_task(
            run_spaceship(self, self.canvas, start_row=center_height, start_column=center_width)
        )
        self.create_task(self.generate_garbage())
        self.create_task(self.show_year())
        self.create_task(self.increase_year_after_delay())
        self.create_task(self.refresh())
        await asyncio.gather(*self.tasks)
