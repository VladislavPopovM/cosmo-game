from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Star:
    row: int
    col: int
    phase: int = 0  # 0..3
    symbol: str = '*'


@dataclass
class Bullet:
    row: float
    col: float


@dataclass
class Garbage:
    row: float
    col: int
    frame: str
    uid: int


@dataclass
class Explosion:
    center_row: int
    center_col: int
    frame_index: int = 0


@dataclass
class Spaceship:
    row: float
    col: float
    frame: str


@dataclass
class Scene:
    stars: List[Star] = field(default_factory=list)
    bullets: List[Bullet] = field(default_factory=list)
    garbages: List[Garbage] = field(default_factory=list)
    explosions: List[Explosion] = field(default_factory=list)
    spaceship: Optional[Spaceship] = None
    year: int = 0
    phrase: Optional[str] = None
    end_text: Optional[str] = None
