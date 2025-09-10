from typing import Protocol


class Collidable(Protocol):
    def has_collision(
        self,
        obj_corner_row: float,
        obj_corner_column: float,
        obj_size_rows: int = 1,
        obj_size_columns: int = 1,
    ) -> bool:
        """Return True if object collides with given area."""
        ...
