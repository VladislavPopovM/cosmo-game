import asyncio
import curses
import random

from core import config
from core.game_scenario import get_garbage_delay_tics, PHRASES
from ui.double_buffer import DoubleBufferedCanvas
from ui.curses_tools import (
    get_garbages_frames,
    get_frame_size,
    sleep,
    get_frame_center_coordinate,
)
from ui.animations import blink, fly_garbage, run_spaceship, SPACESHIP_FRAME
from core.scene import Scene, Star, Garbage, Bullet, Spaceship, Explosion
from ui.render import render_scene


class Game:
    def __init__(self, canvas):
        # Wrap curses canvas with double-buffered proxy for atomic frames
        self.canvas = DoubleBufferedCanvas(canvas)
        self.year = config.START_YEAR
        self.obstacles = []
        self.obstacles_in_last_collisions = []
        self.garbage_frames = get_garbages_frames(config.GARBAGES_PATH)
        self.tasks = []
        self.ended = False
        self.refresh_task = None
        self.scene = Scene(year=self.year)

    def create_task(self, coro):
        task = asyncio.create_task(coro)
        self.tasks.append(task)
        return task

    async def end_game(self):
        if self.ended:
            return
        self.ended = True
        current = asyncio.current_task()

        # Cancel all other tasks except the refresh task and current
        for t in list(self.tasks):
            if t is current or t is self.refresh_task:
                continue
            if not t.done():
                t.cancel()
        # Set end screen text; renderer will show it
        self.scene.end_text = 'The END'

    async def show_year(self):
        while True:
            if self.ended:
                return
            self.scene.year = self.year
            self.scene.phrase = PHRASES.get(self.year)
            await sleep()

    async def increase_year_after_delay(self):
        while True:
            if self.ended:
                return
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
        stars = []
        for _ in range(config.STARS_COUNT):
            row = random.randint(config.BORDER_THICKNESS, height_canvas - config.BORDER_THICKNESS)
            col = random.randint(config.BORDER_THICKNESS, width_canvas - config.BORDER_THICKNESS)
            star = Star(row=row, col=col, phase=random.randint(0, 3), symbol='*')
            self.scene.stars.append(star)
            stars.append(blink(self.canvas, self, star, delay_before_start=random.randint(*config.DELAY_BEFORE_START_BLINK_STAR)))
        return stars

    async def generate_garbage(self):
        while True:
            if self.ended:
                return
            delay_tics = get_garbage_delay_tics(self.year)
            if delay_tics and len(self.obstacles) < config.MAX_GARBAGE:
                self.create_task(self.fill_orbit_with_garbage())
            await sleep(delay_tics or 1)

    async def refresh(self):
        # Draw whole scene and flush once per tick
        while True:
            # Full-frame redraw: clear scene buffer then render
            self.canvas.clear_all()
            render_scene(self.canvas, self.scene)
            self.canvas.flush()
            await asyncio.sleep(config.TIC_TIMEOUT)

    # show_end removed; centralized renderer displays end_text

    async def run(self):
        # Initialize colors for nicer visuals
        curses.start_color()
        try:
            curses.use_default_colors()
        except curses.error:
            pass
        curses.init_pair(config.COLOR_PAIR_STARS, curses.COLOR_YELLOW, -1)
        curses.init_pair(config.COLOR_PAIR_SPACESHIP, curses.COLOR_CYAN, -1)
        curses.init_pair(config.COLOR_PAIR_GARBAGE, curses.COLOR_MAGENTA, -1)
        curses.init_pair(config.COLOR_PAIR_TEXT, curses.COLOR_WHITE, -1)
        curses.init_pair(config.COLOR_PAIR_EXPLOSION, curses.COLOR_RED, -1)

        self.canvas.border()
        self.canvas.nodelay(True)

        for star in self.generate_stars():
            self.create_task(star)

        center_height, center_width = get_frame_center_coordinate(
            self.canvas, SPACESHIP_FRAME
        )
        # Init spaceship in scene
        self.scene.spaceship = Spaceship(row=center_height, col=center_width, frame=SPACESHIP_FRAME)
        self.create_task(run_spaceship(self, self.canvas, start_row=center_height, start_column=center_width))
        self.create_task(self.generate_garbage())
        self.create_task(self.show_year())
        self.create_task(self.increase_year_after_delay())
        self.refresh_task = self.create_task(self.refresh())
        # Swallow task cancellations to avoid bubbling CancelledError
        await asyncio.gather(*self.tasks, return_exceptions=True)
