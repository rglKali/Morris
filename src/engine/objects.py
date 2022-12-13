import dataclasses as dc
import time as tm
from typing import List


@dc.dataclass
class Point:
    player: int
    x: int
    y: int


@dc.dataclass
class Board:
    name: str
    size: int
    move: float
    game: float
    points: list
    connects: List[List[Point]]
    mills: List[List[Point]]
    unite: bool
    skip: bool
