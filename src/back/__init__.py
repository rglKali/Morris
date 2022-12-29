import json
from typing import Optional

from .static import Player, Point, Board, Player


_engine: Optional = None


class Engine:
    def __init__(self):
        self.boards = list()
        for board in json.load(open('data/boards.json')):
            self.new_board(board)

    def new_board(self, data: any([dict, Board])):
        if isinstance(data, dict):
            points = list()
            for point in data['points']:
                points.append(Point(
                    player=None, name=point['name'], neighbors=list(),
                    x='abcdefghi'.index(point['name'][0]) + data['size'] // 2,
                    y='123456789'.index(point['name'][1]) + data['size'] // 2
                ))
            for connect in data['connects']:
                for ind, p1 in enumerate(points):
                    for p2 in points[:ind]:
                        if p1.name in connect and p2.name in connect:
                            p1.neighbors.append(p2)
                            p2.neighbors.append(p1)
            self.boards.append(Board(
                name=data['name'],
                size=data['size'],
                move=None,
                game=None,
                points=points,
                pieces=data['pieces'],
                unite=data['unite'],
                skip=data['skip']
            ))
        else:
            self.boards.append(data)

    def start_new_game(self, name: str):
        for board in self.boards:
            if board.name == name:
                return Game(board)


class Game:
    def __init__(self, board: 'Board'):
        self.board = board

    def new_player(self):
        pass

    def get_possible_moves(self, point: 'Point' = None):
        if point is None:
            pass

    def move_piece(self):
        pass

    def set_piece(self):
        pass

    def remove_piece(self):
        pass


def run():
    pass
