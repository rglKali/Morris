import dataclasses as dc


@dc.dataclass
class Player:
    turn: bool
    token: str
    game: any([int, None])
    move: any([int, None])
    pieces: int
    phase: int
    history: list


@dc.dataclass
class Point:
    player: any(['Player', None])
    location: list[int]
    neighbors: list['Point']


@dc.dataclass
class Board:
    name: str
    size: int
    move: float
    game: float
    points: list['Point']
    pieces: int
    unite: bool
    skip: bool
