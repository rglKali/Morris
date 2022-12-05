from .objects import Board, Player
import json


class BoardNotExists(Exception):
    pass


class Engine:
    def __init__(self):
        self.board = None
        self.players = [Player, Player]
        self.pieces = None

    def open_board(self, name: str):
        boards = json.load(open('res/boards.json'))
        board = [board for board in boards if board['name'] == name]
        if not len(board):
            raise BoardNotExists
        else:
            self.board = Board(board[0])

    def load_board(self, data: dict):
        self.board = Board(data)

    def save_game(self):
        pass

    def load_game(self):
        pass

    def get_moves(self):
        pass

    def move(self):
        pass
