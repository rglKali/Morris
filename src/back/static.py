import dataclasses as dc

__all__ = [
    'Player',
    'Point',
    'Board'
]


@dc.dataclass
class Action:
    player: 'Player'
    action: any(['move', 'set', 'remove'])
    from_point: 'Point'
    to_point: 'Point'


@dc.dataclass
class Player:
    turn: bool
    token: str
    game: any([int, None])
    move: any([int, None])
    pieces: int
    phase: int
    history: list[Action]


@dc.dataclass
class Point:
    player: any(['Player', None])
    name: str
    x: int
    y: int
    neighbors: list['Point']


@dc.dataclass
class Board:
    name: str
    size: int
    move: any([int, None])
    game: any([int, None])
    points: list['Point']
    pieces: int
    unite: bool
    skip: bool
