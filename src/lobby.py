from . import pytk as tk
from .data import Board, Player

__all__ = ['Lobby']


class lang:
    pass


class Lobby(tk.View):
    def __init__(self, board: 'Board', host: 'Player' = None):
        self.board = board
        self.host = host if host else Player()
        super().__init__()

    def on_key_press(self, key: str):
        from .game import Game
        self.window.view = Game(self.board, [self.host])

    def on_mouse_press(self, x: int, y: int, key):
        from .game import Game
        self.window.view = Game(self.board, [self.host])

    def on_draw(self):
        tk.draw_text(360, 240, 'Dev')
